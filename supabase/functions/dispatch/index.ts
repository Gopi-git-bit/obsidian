import { getServiceClient, jsonResponse, errorResponse } from "../_shared/supabase-client.ts";

/**
 * POST /functions/v1/dispatch
 * Actions:
 *   - "search": find eligible vehicles for an order and create offers
 *   - "offer": create a dispatch offer to a specific driver/vehicle
 *   - "respond": driver accepts/rejects an offer
 *
 * Body:
 *   action: 'search' | 'offer' | 'respond'
 *   order_id: UUID
 *   -- for offer --
 *   driver_id?: UUID
 *   vehicle_id?: UUID
 *   vendor_id?: UUID
 *   -- for respond --
 *   offer_id?: UUID
 *   response: 'accepted' | 'rejected'
 */

interface DispatchPayload {
  action: "search" | "offer" | "respond";
  order_id: string;
  driver_id?: string;
  vehicle_id?: string;
  vendor_id?: string;
  offer_id?: string;
  response?: "accepted" | "rejected";
}

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") {
    return errorResponse("Method not allowed", 405);
  }

  let body: DispatchPayload;
  try {
    body = await req.json();
  } catch (_e) {
    return errorResponse("Invalid JSON body");
  }

  if (!body.order_id || !body.action) {
    return errorResponse("Missing order_id or action");
  }

  const supabase = getServiceClient();

  const { data: order, error: orderError } = await supabase
    .from("orders")
    .select("*, material_types!inner(required_body, max_weight_tons)")
    .eq("id", body.order_id)
    .single();

  if (orderError || !order) {
    return errorResponse("Order not found", 404);
  }

  if (body.action === "search") {
    // SOP Step 1: same-city, idle, online, body + weight match, valid docs.
    const { data: candidates, error: searchError } = await supabase.rpc(
      "find_dispatch_candidates",
      {
        p_order_id: order.id,
        p_radius_km: 25,
      }
    );

    if (searchError) {
      console.error("Dispatch search error:", searchError);
      return errorResponse("Failed to search dispatch candidates", 500);
    }

    // Mark order as in vehicle_search.
    await supabase
      .from("orders")
      .update({ status: "vehicle_search", updated_at: new Date().toISOString() })
      .eq("id", order.id);

    await logEvent(supabase, order.id, "dispatch.search_completed", {
      candidates_found: (candidates as unknown[])?.length ?? 0,
    });

    return jsonResponse({
      success: true,
      order_id: order.id,
      status: "vehicle_search",
      candidates: candidates ?? [],
    });
  }

  if (body.action === "offer") {
    if (!body.driver_id || !body.vehicle_id) {
      return errorResponse("driver_id and vehicle_id required for offer");
    }

    const expiresAt = new Date(Date.now() + 3 * 60 * 1000).toISOString(); // 3 min offer

    const { data: offer, error: offerError } = await supabase
      .from("dispatch_offers")
      .insert({
        order_id: order.id,
        driver_id: body.driver_id,
        vehicle_id: body.vehicle_id,
        vendor_id: body.vendor_id ?? null,
        expires_at: expiresAt,
        status: "pending",
      })
      .select()
      .single();

    if (offerError || !offer) {
      console.error("Offer insert error:", offerError);
      return errorResponse("Failed to create dispatch offer", 500);
    }

    await logEvent(supabase, order.id, "dispatch.offer_sent", {
      offer_id: offer.id,
      driver_id: body.driver_id,
      expires_at: expiresAt,
    });

    return jsonResponse({ success: true, offer }, 201);
  }

  if (body.action === "respond") {
    if (!body.offer_id || !body.response) {
      return errorResponse("offer_id and response required");
    }

    const { data: offer, error: offerError } = await supabase
      .from("dispatch_offers")
      .select("*, orders!inner(id, status)")
      .eq("id", body.offer_id)
      .single();

    if (offerError || !offer) {
      return errorResponse("Offer not found", 404);
    }

    if (offer.status !== "pending") {
      return errorResponse("Offer already responded", 409);
    }

    const respondedAt = new Date().toISOString();

    if (body.response === "rejected" || new Date(offer.expires_at) < new Date()) {
      await supabase
        .from("dispatch_offers")
        .update({
          status: body.response === "rejected" ? "rejected" : "expired",
          responded_at: respondedAt,
        })
        .eq("id", body.offer_id);

      await logEvent(supabase, order.id, "dispatch.offer_declined", {
        offer_id: body.offer_id,
        response: body.response,
      });

      return jsonResponse({ success: true, status: offer.status });
    }

    // Accepted: assign vehicle/driver to order and transition state.
    const { error: assignError } = await supabase
      .from("orders")
      .update({
        status: "driver_assigned",
        assigned_vehicle_id: offer.vehicle_id,
        assigned_driver_id: offer.driver_id,
        updated_at: respondedAt,
      })
      .eq("id", order.id);

    if (assignError) {
      console.error("Assign error:", assignError);
      return errorResponse("Failed to assign order", 500);
    }

    // Mark vehicle as in_shipment and driver as in_shipment.
    await supabase
      .from("vehicles")
      .update({ current_status: "in_shipment", updated_at: respondedAt })
      .eq("id", offer.vehicle_id);

    await supabase
      .from("drivers")
      .update({ current_status: "in_shipment", updated_at: respondedAt })
      .eq("id", offer.driver_id);

    await supabase
      .from("dispatch_offers")
      .update({ status: "accepted", responded_at: respondedAt })
      .eq("id", body.offer_id);

    await logEvent(supabase, order.id, "dispatch.accepted", {
      offer_id: body.offer_id,
      driver_id: offer.driver_id,
      vehicle_id: offer.vehicle_id,
    });

    return jsonResponse({
      success: true,
      order_id: order.id,
      status: "driver_assigned",
    });
  }

  return errorResponse("Unknown action");
});

async function logEvent(
  supabase: ReturnType<typeof getServiceClient>,
  orderId: string,
  eventType: string,
  payload: Record<string, unknown>
) {
  await supabase.from("order_event_log").insert({
    order_id: orderId,
    event_type: eventType,
    payload,
    source: "edge_function",
  });
}
