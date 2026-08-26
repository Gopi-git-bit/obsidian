import { getServiceClient, jsonResponse, errorResponse } from "../_shared/supabase-client.ts";

/**
 * POST /functions/v1/payment-hold
 * Actions:
 *   - "create": place a hold on a payment (requires admin)
 *   - "release": release a hold (requires admin)
 *   - "check": check if a payment has active holds
 *
 * Body:
 *   action: 'create' | 'release' | 'check'
 *   payment_id: UUID
 *   -- for create --
 *   hold_reason?: 'missing_pod' | 'theft_investigation' | 'damage_claim' | 'dispute' | 'admin_review' | 'legal_issue'
 *   held_amount?: number
 *   -- for release --
 *   release_reason?: string
 */

interface PaymentHoldPayload {
  action: "create" | "release" | "check";
  payment_id: string;
  hold_reason?: string;
  held_amount?: number;
  release_reason?: string;
}

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") {
    return errorResponse("Method not allowed", 405);
  }

  let body: PaymentHoldPayload;
  try {
    body = await req.json();
  } catch (_e) {
    return errorResponse("Invalid JSON body");
  }

  if (!body.payment_id || !body.action) {
    return errorResponse("Missing payment_id or action");
  }

  const supabase = getServiceClient();

  // Verify payment exists.
  const { data: payment, error: paymentError } = await supabase
    .from("payments")
    .select("id, order_id, amount, status")
    .eq("id", body.payment_id)
    .single();

  if (paymentError || !payment) {
    return errorResponse("Payment not found", 404);
  }

  if (body.action === "check") {
    const { data: holds, error: holdsError } = await supabase
      .from("payment_holds")
      .select("*")
      .eq("payment_id", body.payment_id)
      .is("released_at", null);

    if (holdsError) {
      return errorResponse("Failed to fetch holds", 500);
    }

    const totalHeld = (holds ?? []).reduce(
      (sum, h) => sum + Number(h.held_amount),
      0
    );

    return jsonResponse({
      payment_id: payment.id,
      active_holds: holds ?? [],
      total_held: totalHeld,
      has_active_holds: (holds ?? []).length > 0,
    });
  }

  // Admin-only actions below: create / release.
  const authHeader = req.headers.get("Authorization");
  if (!authHeader) {
    return errorResponse("Authorization header required", 401);
  }

  const { data: { user }, error: authError } = await supabase.auth.getUser(
    authHeader.replace("Bearer ", "")
  );

  if (authError || !user) {
    return errorResponse("Invalid authentication", 401);
  }

  const { data: adminUser, error: adminError } = await supabase
    .from("users")
    .select("id, role")
    .eq("id", user.id)
    .single();

  if (adminError || adminUser?.role !== "admin") {
    return errorResponse("Admin access required", 403);
  }

  if (body.action === "create") {
    if (!body.hold_reason || body.held_amount == null) {
      return errorResponse("hold_reason and held_amount required");
    }

    if (body.held_amount > Number(payment.amount)) {
      return errorResponse("Hold amount cannot exceed payment amount", 422);
    }

    const { data: hold, error: holdError } = await supabase
      .from("payment_holds")
      .insert({
        payment_id: payment.id,
        hold_reason: body.hold_reason,
        held_amount: body.held_amount,
        held_by: adminUser.id,
      })
      .select()
      .single();

    if (holdError || !hold) {
      console.error("Hold insert error:", holdError);
      return errorResponse("Failed to create payment hold", 500);
    }

    await logEvent(supabase, payment.order_id, "payment.hold_created", {
      payment_id: payment.id,
      hold_id: hold.id,
      hold_reason: body.hold_reason,
      held_amount: body.held_amount,
    });

    return jsonResponse({ success: true, hold }, 201);
  }

  if (body.action === "release") {
    const { data: activeHolds, error: activeError } = await supabase
      .from("payment_holds")
      .select("id")
      .eq("payment_id", body.payment_id)
      .is("released_at", null)
      .order("held_at", { ascending: false })
      .limit(1);

    if (activeError || !activeHolds || activeHolds.length === 0) {
      return errorResponse("No active hold to release", 404);
    }

    const { error: releaseError } = await supabase
      .from("payment_holds")
      .update({
        released_at: new Date().toISOString(),
        release_reason: body.release_reason ?? "Admin release",
        released_by: adminUser.id,
      })
      .eq("id", activeHolds[0].id);

    if (releaseError) {
      return errorResponse("Failed to release hold", 500);
    }

    await logEvent(supabase, payment.order_id, "payment.hold_released", {
      payment_id: payment.id,
      hold_id: activeHolds[0].id,
      release_reason: body.release_reason,
    });

    return jsonResponse({ success: true, released_hold_id: activeHolds[0].id });
  }

  return errorResponse("Unknown action");
});

async function logEvent(
  supabase: ReturnType<typeof getServiceClient>,
  orderId: string | null,
  eventType: string,
  payload: Record<string, unknown>
) {
  if (!orderId) return;
  await supabase.from("order_event_log").insert({
    order_id: orderId,
    event_type: eventType,
    payload,
    source: "edge_function",
  });
}
