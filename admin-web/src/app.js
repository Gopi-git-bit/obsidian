import { ZippyAdminApi } from "./api/generated-client.js";

const state = {
  api: null,
  token: sessionStorage.getItem("zippyAdminToken") || "",
  orders: [],
  selectedOrder: null,
  flow: null,
  events: null
};

const els = {
  apiBase: document.querySelector("#apiBase"),
  devLogin: document.querySelector("#devLogin"),
  loginStatus: document.querySelector("#loginStatus"),
  refreshOrders: document.querySelector("#refreshOrders"),
  ordersStatus: document.querySelector("#ordersStatus"),
  ordersList: document.querySelector("#ordersList"),
  emptyState: document.querySelector("#emptyState"),
  orderDetail: document.querySelector("#orderDetail"),
  detailTitle: document.querySelector("#detailTitle"),
  detailRoute: document.querySelector("#detailRoute"),
  lifecycleBadge: document.querySelector("#lifecycleBadge"),
  actions: document.querySelector("#actions"),
  flowSteps: document.querySelector("#flowSteps"),
  missingSteps: document.querySelector("#missingSteps"),
  recordSections: document.querySelector("#recordSections"),
  auditTrail: document.querySelector("#auditTrail")
};

function api() {
  const baseUrl = els.apiBase.value.trim() || "http://localhost:8000";
  if (!state.api || state.api.baseUrl !== baseUrl.replace(/\/$/, "")) {
    state.api = new ZippyAdminApi(baseUrl, state.token);
  }
  state.api.setToken(state.token);
  return state.api;
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "-";
  return String(value);
}

function pretty(value) {
  return JSON.stringify(value, null, 2);
}

function orderLabel(order) {
  return `${order.origin_city} -> ${order.destination_city}`;
}

function setStatus(message) {
  els.ordersStatus.textContent = message;
}

function setLoginStatus(message) {
  els.loginStatus.textContent = message;
}

async function devLogin() {
  const data = await api().devLogin({
    username: "admin-web-dev",
    password: "admin-web-dev",
    role: "super_admin"
  });
  state.token = data.access_token;
  sessionStorage.setItem("zippyAdminToken", state.token);
  api().setToken(state.token);
  setLoginStatus(`Signed in as ${data.role}`);
}

async function ensureDevLogin() {
  if (state.token) {
    setLoginStatus("Signed in");
    return;
  }
  await devLogin();
}

function renderOrders() {
  els.ordersList.innerHTML = "";
  for (const order of state.orders) {
    const row = document.createElement("button");
    row.type = "button";
    row.className = `order-row${state.selectedOrder?.id === order.id ? " active" : ""}`;
    row.innerHTML = `
      <span class="row-main">
        <strong>${order.shipper_name}</strong>
        <span>${order.current_state}</span>
      </span>
      <span class="row-sub">${orderLabel(order)}</span>
      <span class="row-sub">${order.id}</span>
    `;
    row.addEventListener("click", () => loadOrder(order.id));
    els.ordersList.append(row);
  }
}

function renderFlowSteps() {
  els.flowSteps.innerHTML = "";
  const steps = state.flow?.steps || [];
  for (const step of steps) {
    const item = document.createElement("div");
    item.className = `step ${step.status}`;
    item.innerHTML = `<strong>${step.step.replaceAll("_", " ")}</strong><br><span>${step.status}</span>`;
    els.flowSteps.append(item);
  }
  const missing = state.flow?.missing_steps || [];
  els.missingSteps.textContent = missing.length
    ? `Missing or failed steps: ${missing.join(", ")}`
    : "No missing flow steps detected.";
}

function addRecordSection(title, value) {
  const card = document.createElement("div");
  card.className = "record-card";
  card.innerHTML = `<strong>${title}</strong><pre>${pretty(value)}</pre>`;
  els.recordSections.append(card);
}

function renderRecords() {
  els.recordSections.innerHTML = "";
  const flow = state.flow || {};
  addRecordSection("Quote", flow.quote_records || []);
  addRecordSection("Match", flow.matches || []);
  addRecordSection("Trip", flow.trip || null);
  addRecordSection("Payment", flow.payment_records || []);
  addRecordSection("Loading Photo", flow.loading_photos || []);
  addRecordSection("Milestone", flow.milestones || []);
  addRecordSection("POD", flow.pod_records || []);
  addRecordSection("OTP", { otp_verified: flow.trip?.otp_verified === "true" });
  addRecordSection("Settlement", flow.settlement_records || []);
  addRecordSection("Journal Entry", flow.journal_entries || []);
  addRecordSection("GST Invoice", flow.gst_invoice_records || []);
}

function renderAuditTrail() {
  els.auditTrail.innerHTML = "";
  const events = state.events?.events || [];
  if (!events.length) {
    els.auditTrail.textContent = "No audit events recorded.";
    return;
  }
  for (const event of events) {
    const item = document.createElement("div");
    item.className = "audit-item";
    item.innerHTML = `
      <strong>${event.event_name}</strong>
      <div>${event.from_state} -> ${event.to_state}</div>
      <div class="row-sub">${formatValue(event.actor_role)} | ${formatValue(event.trace_id)}</div>
    `;
    els.auditTrail.append(item);
  }
}

function actionButton(label, handler, disabled = false) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = label;
  button.disabled = disabled;
  button.addEventListener("click", handler);
  return button;
}

function transitionPayload(toState, event, actorRole, payload = {}) {
  return {
    to_state: toState,
    event,
    payload,
    actor_role: actorRole,
    idempotency_key: crypto.randomUUID(),
    trace_id: `admin-web-${crypto.randomUUID()}`
  };
}

function promptRequired(label, fallback = "") {
  const value = window.prompt(label, fallback);
  if (!value) throw new Error(`${label} is required`);
  return value;
}

async function runAction(handler) {
  try {
    await handler();
    await loadOrder(state.selectedOrder.id);
  } catch (error) {
    window.alert(error.message || String(error));
  }
}

function renderActions() {
  els.actions.innerHTML = "";
  const order = state.selectedOrder;
  const flow = state.flow;
  if (!order || !flow) return;

  const tripId = flow.trip?.trip_id;
  const firstProposedMatch = (flow.matches || []).find((match) => match.status === "proposed");
  const firstAcceptedMatch = (flow.matches || []).find((match) => match.status === "accepted");
  const vehicleId = flow.trip?.vehicle_id || firstAcceptedMatch?.vehicle_id || firstProposedMatch?.vehicle_id;

  els.actions.append(
    actionButton(
      "Confirm Order",
      () => runAction(() => api().transitionOrder(order.id, transitionPayload("CONFIRMED", "order_submitted", "OMS", {
        payment_mode: order.payment_mode || "advance",
        topay_consent_status: order.topay_consent_status || "not_required",
        material_type: order.material_type || "general_goods",
        body_type_required: order.body_type_required || "open"
      }))),
      order.current_state !== "CREATED"
    ),
    actionButton("Generate Quote", () => runAction(() => api().createQuote(order.id))),
    actionButton("Find Matches", () => runAction(() => api().findMatches(order.id, { limit: 5, min_score: 0 }))),
    actionButton(
      "Accept Match",
      () => runAction(() => api().acceptMatch(firstProposedMatch.id, { notes: "Admin accepted proposed match" })),
      !firstProposedMatch
    ),
    actionButton(
      "Record Advance",
      () => runAction(() => api().recordAdvancePayment(order.id, {
        amount: Number(promptRequired("Advance amount", "9000")),
        currency: "INR",
        provider_ref: promptRequired("Provider reference", "manual-admin"),
        idempotency_key: `admin-advance-${crypto.randomUUID()}`
      })),
      !tripId && !firstAcceptedMatch
    ),
    actionButton(
      "Start Pickup",
      () => runAction(() => api().transitionOrder(order.id, transitionPayload("EN_ROUTE_TO_PICKUP", "driver_started_pickup", "DRIVER"))),
      order.current_state !== "ASSIGNED"
    ),
    actionButton(
      "Arrived Pickup",
      () => runAction(() => api().transitionOrder(order.id, transitionPayload("AT_PICKUP_WAITING", "driver_arrived_pickup", "DRIVER"))),
      order.current_state !== "EN_ROUTE_TO_PICKUP"
    ),
    actionButton(
      "Start Loading",
      () => runAction(() => api().transitionOrder(order.id, transitionPayload("LOADING", "shipment_doc_scanned", "DRIVER", {
        driver_id: "admin-driver",
        vehicle_id: vehicleId,
        doc_type: "loading_photo",
        doc_url: "s3://docs/loading.jpg",
        scan_exif: {}
      }))),
      order.current_state !== "AT_PICKUP_WAITING" || !vehicleId
    ),
    actionButton(
      "Upload Loading Photo",
      () => runAction(() => api().uploadLoadingPhoto(tripId, {
        photo_url: promptRequired("Loading photo URL", "s3://docs/loading.jpg"),
        uploaded_by: promptRequired("Uploaded by", "admin"),
        idempotency_key: `admin-loading-${crypto.randomUUID()}`
      })),
      !tripId
    ),
    actionButton(
      "Depart Delivery",
      () => runAction(() => api().transitionOrder(order.id, transitionPayload("DEPARTED_FOR_DELIVERY", "loading_completed", "DRIVER"))),
      order.current_state !== "LOADING"
    ),
    actionButton(
      "Add Milestone",
      () => runAction(() => api().recordTripMilestone(tripId, {
        milestone_type: promptRequired("Milestone type", "in_transit"),
        status: "recorded",
        payload: {},
        idempotency_key: `admin-mile-${crypto.randomUUID()}`
      })),
      !tripId
    ),
    actionButton(
      "Arrive Delivery",
      () => runAction(() => api().transitionOrder(order.id, transitionPayload("AT_DELIVERY_WAITING", "driver_arrived_delivery", "DRIVER"))),
      order.current_state !== "DEPARTED_FOR_DELIVERY"
    ),
    actionButton(
      "Upload POD",
      () => runAction(() => api().uploadPod(tripId, {
        pod_url: promptRequired("POD URL", "s3://docs/pod.jpg"),
        consignee_otp: promptRequired("Consignee OTP", "123456"),
        pod_exif: {},
        uploaded_by: promptRequired("Uploaded by", "admin"),
        idempotency_key: `admin-pod-${crypto.randomUUID()}`
      })),
      !tripId
    ),
    actionButton(
      "Verify POD",
      () => runAction(() => api().verifyPod(tripId, {
        verified_by: promptRequired("Verified by", "rag-ocr"),
        idempotency_key: `admin-pod-verify-${crypto.randomUUID()}`
      })),
      !tripId
    ),
    actionButton(
      "Verify OTP",
      () => runAction(() => api().verifyOtp(tripId, {
        otp: promptRequired("OTP", "123456"),
        verified_by: promptRequired("Verified by", "admin"),
        idempotency_key: `admin-otp-${crypto.randomUUID()}`
      })),
      !tripId
    ),
    actionButton(
      "Release Settlement",
      () => runAction(() => api().releaseSettlement(tripId, {
        amount: Number(promptRequired("Settlement amount", "18000")),
        commission_amount: Number(promptRequired("Commission amount", "1800")),
        gst_amount: Number(promptRequired("GST amount", "324")),
        driver_payable_amount: Number(promptRequired("Driver payable", "16200")),
        currency: "INR",
        idempotency_key: `admin-settlement-${crypto.randomUUID()}`,
        trace_id: `admin-settlement-${crypto.randomUUID()}`,
        confidence_score: 0.91,
        decision_reason: "Admin settlement release preflight",
        evidence_refs: ["pod:verified", "otp:verified"]
      })),
      !tripId
    )
  );
}

function renderDetail() {
  const order = state.selectedOrder;
  els.emptyState.classList.toggle("hidden", Boolean(order));
  els.orderDetail.classList.toggle("hidden", !order);
  if (!order) return;

  els.detailTitle.textContent = `Order ${order.id}`;
  els.detailRoute.textContent = `${order.shipper_name} | ${orderLabel(order)} | ${order.weight_kg} kg`;
  els.lifecycleBadge.textContent = order.current_state;
  renderActions();
  renderFlowSteps();
  renderRecords();
  renderAuditTrail();
}

async function loadOrders() {
  setStatus("Loading orders...");
  try {
    await ensureDevLogin();
    const data = await api().listOrders({ limit: 100 });
    state.orders = data.orders || [];
    setStatus(`${data.total || state.orders.length} orders`);
    renderOrders();
  } catch (error) {
    setStatus(`Could not load orders: ${error.message}`);
  }
}

async function loadOrder(orderId) {
  const [order, flow, events] = await Promise.all([
    api().getOrder(orderId),
    api().getOrderFlowSummary(orderId),
    api().getOrderEvents(orderId)
  ]);
  state.selectedOrder = order;
  state.flow = flow;
  state.events = events;
  renderOrders();
  renderDetail();
}

els.refreshOrders.addEventListener("click", loadOrders);
els.apiBase.addEventListener("change", loadOrders);
els.devLogin.addEventListener("click", async () => {
  try {
    await devLogin();
    await loadOrders();
  } catch (error) {
    window.alert(error.message || String(error));
  }
});

loadOrders();
