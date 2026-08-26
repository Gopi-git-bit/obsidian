import { getServiceClient, jsonResponse, errorResponse } from "../_shared/supabase-client.ts";

/**
 * POST /functions/v1/order-create
 * Body:
 *   customer_user_id: UUID       (Supabase auth user id)
 *   origin_city_id: UUID
 *   destination_city_id: UUID
 *   origin_pincode: string
 *   destination_pincode: string
 *   material_type_id: UUID
 *   cargo_weight_tons: number
 *   cargo_volume_cbm?: number
 *   declared_value?: number
 *   service_tier?: 'standard' | 'express' | 'premium'
 *   delivery_type?: 'normal' | 'express'
 *   load_type?: 'full_load' | 'part_load' | 'multi_spot'
 *   scheduled_pickup_at?: ISO timestamp
 *   consignee_name?: string
 *   consignee_phone?: string
 *   consignee_address?: string
 *
 * State-machine rule: creates order in 'draft' status.
 */

interface OrderPayload {
  customer_user_id: string;
  origin_city_id: string;
  destination_city_id: string;
  origin_pincode: string;
  destination_pincode: string;
  material_type_id: string;
  cargo_weight_tons: number;
  cargo_volume_cbm?: number;
  declared_value?: number;
  service_tier?: string;
  delivery_type?: string;
  load_type?: string;
  scheduled_pickup_at?: string;
  consignee_name?: string;
  consignee_phone?: string;
  consignee_address?: string;
}

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") {
    return errorResponse("Method not allowed", 405);
  }

  let body: OrderPayload;
  try {
    body = await req.json();
  } catch (_e) {
    return errorResponse("Invalid JSON body");
  }

  const required = [
    "customer_user_id",
    "origin_city_id",
    "destination_city_id",
    "origin_pincode",
    "destination_pincode",
    "material_type_id",
    "cargo_weight_tons",
  ];

  for (const key of required) {
    if (body[key as keyof OrderPayload] == null) {
      return errorResponse(`Missing required field: ${key}`);
    }
  }

  const supabase = getServiceClient();

  // Resolve customer profile from auth user id.
  const { data: customer, error: customerError } = await supabase
    .from("customers")
    .select("id, city_id, payment_terms_type")
    .eq("user_id", body.customer_user_id)
    .single();

  if (customerError || !customer) {
    return errorResponse("Customer profile not found for this user", 404);
  }

  // Validate material type and max weight.
  const { data: material, error: materialError } = await supabase
    .from("material_types")
    .select("id, required_body, max_weight_tons, is_hazardous")
    .eq("id", body.material_type_id)
    .single();

  if (materialError || !material) {
    return errorResponse("Invalid material type", 400);
  }

  if (material.max_weight_tons != null && body.cargo_weight_tons > material.max_weight_tons) {
    return errorResponse(
      `Cargo weight exceeds material limit of ${material.max_weight_tons} tons`,
      422
    );
  }

  // Generate order number: ZIP-YYYY-XXXXXX
  const year = new Date().getFullYear();
  const { data: seq, error: seqError } = await supabase.rpc("next_order_number", {
    year_str: String(year),
  });

  if (seqError) {
    console.error("Sequence error:", seqError);
    return errorResponse("Failed to generate order number", 500);
  }

  const orderNumber = `ZIP-${year}-${String(seq).padStart(6, "0")}`;

  const insert = {
    order_number: orderNumber,
    customer_id: customer.id,
    origin_city_id: body.origin_city_id,
    destination_city_id: body.destination_city_id,
    origin_pincode: body.origin_pincode,
    destination_pincode: body.destination_pincode,
    material_type_id: body.material_type_id,
    cargo_weight_tons: body.cargo_weight_tons,
    cargo_volume_cbm: body.cargo_volume_cbm ?? null,
    declared_value: body.declared_value ?? 0,
    service_tier: body.service_tier ?? "standard",
    delivery_type: body.delivery_type ?? "normal",
    load_type: body.load_type ?? "full_load",
    scheduled_pickup_at: body.scheduled_pickup_at ?? null,
    consignee_name: body.consignee_name ?? null,
    consignee_phone: body.consignee_phone ?? null,
    consignee_address: body.consignee_address ?? null,
    status: "draft",
    payment_status: "pending",
  };

  const { data: order, error: insertError } = await supabase
    .from("orders")
    .insert(insert)
    .select()
    .single();

  if (insertError || !order) {
    console.error("Order insert error:", insertError);
    return errorResponse("Failed to create order", 500);
  }

  // Log the event for Realtime subscribers.
  await supabase.from("order_event_log").insert({
    order_id: order.id,
    event_type: "order_draft_created",
    payload: { order_number: order.order_number, status: order.status },
    source: "edge_function",
  });

  return jsonResponse({
    success: true,
    order_id: order.id,
    order_number: order.order_number,
    status: order.status,
  }, 201);
});
