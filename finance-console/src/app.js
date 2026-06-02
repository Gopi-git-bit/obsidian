import { ZippyFinanceApi } from "./api/generated-client.js";

const state = {
  api: null,
  token: sessionStorage.getItem("zippyFinanceToken") || "",
  username: sessionStorage.getItem("zippyFinanceUsername") || "finance-console-dev",
  role: sessionStorage.getItem("zippyFinanceRole") || "finance_admin",
  settlements: [],
  selected: null
};

const els = {
  apiBase: document.querySelector("#apiBase"),
  username: document.querySelector("#username"),
  role: document.querySelector("#role"),
  login: document.querySelector("#login"),
  loginStatus: document.querySelector("#loginStatus"),
  refresh: document.querySelector("#refresh"),
  queueStatus: document.querySelector("#queueStatus"),
  settlementList: document.querySelector("#settlementList"),
  emptyState: document.querySelector("#emptyState"),
  settlementDetail: document.querySelector("#settlementDetail"),
  detailTitle: document.querySelector("#detailTitle"),
  detailSub: document.querySelector("#detailSub"),
  releaseBadge: document.querySelector("#releaseBadge"),
  blocker: document.querySelector("#blocker"),
  releaseSettlement: document.querySelector("#releaseSettlement"),
  readiness: document.querySelector("#readiness"),
  accounting: document.querySelector("#accounting"),
  records: document.querySelector("#records"),
  auditTrail: document.querySelector("#auditTrail"),
  outboxEvents: document.querySelector("#outboxEvents")
};

els.username.value = state.username;
els.role.value = state.role;

function api() {
  const baseUrl = els.apiBase.value.trim() || "http://127.0.0.1:8000";
  if (!state.api || state.api.baseUrl !== baseUrl.replace(/\/$/, "")) {
    state.api = new ZippyFinanceApi(baseUrl, state.token);
  }
  state.api.setToken(state.token);
  return state.api;
}

function pretty(value) { return JSON.stringify(value, null, 2); }
function yesNo(value) { return value ? "yes" : "no"; }

function blockerCodeFromError(error) {
  const detail = error.payload?.detail;
  if (detail?.blocker === "fraud_hold") return "FRAUD_HOLD_ACTIVE";
  if (detail?.blocker === "settlement_hold") return "SETTLEMENT_HOLD_ACTIVE";
  const message = detail?.message || detail || error.message || "";
  if (/POD/i.test(message)) return "POD_NOT_VERIFIED";
  if (/OTP/i.test(message)) return "OTP_NOT_VERIFIED";
  if (error.status === 403) return "WRONG_ROLE";
  return String(message);
}

async function login() {
  const username = els.username.value.trim() || "finance-console-dev";
  const role = els.role.value || "finance_admin";
  const data = await api().devLogin({ username, password: "finance-console-dev", role });
  state.token = data.access_token;
  state.username = username;
  state.role = role;
  sessionStorage.setItem("zippyFinanceToken", state.token);
  sessionStorage.setItem("zippyFinanceUsername", username);
  sessionStorage.setItem("zippyFinanceRole", role);
  api().setToken(state.token);
  els.loginStatus.textContent = `Signed in as ${data.username} (${data.role})`;
}

async function ensureLogin() {
  if (state.token) {
    els.loginStatus.textContent = `Signed in as ${state.username} (${state.role})`;
    return;
  }
  await login();
}

function renderList() {
  els.settlementList.innerHTML = "";
  for (const item of state.settlements) {
    const row = document.createElement("button");
    row.className = `row${state.selected?.trip_id === item.trip_id ? " active" : ""}`;
    row.type = "button";
    row.innerHTML = `
      <span class="row-main"><strong>${item.release_status}</strong><span>${item.blocker_code || (item.release_eligible ? "ELIGIBLE" : "REVIEW")}</span></span>
      <span class="row-sub">trip ${item.trip_id}</span>
      <span class="row-sub">order ${item.order_id} | POD ${item.pod_status} | OTP ${yesNo(item.otp_verified)}</span>
    `;
    row.addEventListener("click", () => loadSettlement(item.trip_id));
    els.settlementList.append(row);
  }
}

function metric(target, title, value) {
  const el = document.createElement("div");
  el.className = "metric";
  el.innerHTML = `<span>${title}</span><strong>${value ?? "-"}</strong>`;
  target.append(el);
}

function card(title, value) {
  const el = document.createElement("div");
  el.className = "record-card";
  el.innerHTML = `<strong>${title}</strong><pre>${pretty(value)}</pre>`;
  els.records.append(el);
}

function renderDetail() {
  const item = state.selected;
  els.emptyState.classList.toggle("hidden", Boolean(item));
  els.settlementDetail.classList.toggle("hidden", !item);
  if (!item) return;

  els.detailTitle.textContent = `Trip ${item.trip_id}`;
  els.detailSub.textContent = `order ${item.order_id} | customer ${item.customer_id || "-"}`;
  els.releaseBadge.textContent = item.release_status;
  els.blocker.classList.toggle("hidden", !item.blocker_code);
  els.blocker.textContent = item.blocker_code ? `${item.blocker_code}: ${item.blocker_reason || "Blocked"}` : "";
  els.releaseSettlement.disabled = !item.release_eligible || !["finance_admin", "super_admin"].includes(state.role);

  els.readiness.innerHTML = "";
  metric(els.readiness, "POD verified", yesNo(item.pod_verified));
  metric(els.readiness, "OTP verified", yesNo(item.otp_verified));
  metric(els.readiness, "Fraud hold active", yesNo(item.fraud_hold_active));
  metric(els.readiness, "Settlement hold active", yesNo(item.settlement_hold_active));
  metric(els.readiness, "Release eligible", yesNo(item.release_eligible));
  metric(els.readiness, "Blocker reason", item.blocker_reason || "-");

  els.accounting.innerHTML = "";
  metric(els.accounting, "journal_created", yesNo(item.journal_created));
  metric(els.accounting, "gst_invoice_created", yesNo(item.gst_invoice_created));
  metric(els.accounting, "journal_id", item.journal_id || "-");
  metric(els.accounting, "gst_invoice_id", item.gst_invoice_id || "-");

  els.records.innerHTML = "";
  card("Settlement", item.settlement || { status: item.release_status, amount: item.amount, currency: item.currency });
  card("Fraud Holds", item.fraud_holds || []);
  card("Settlement Holds", item.settlement_holds || []);

  els.auditTrail.innerHTML = "";
  for (const audit of item.audit_trail || []) {
    const row = document.createElement("div");
    row.className = "audit-item";
    row.textContent = `${audit.milestone_type} | ${audit.status} | ${audit.recorded_at || ""}`;
    els.auditTrail.append(row);
  }

  els.outboxEvents.innerHTML = "";
  for (const event of item.outbox_events || []) {
    const row = document.createElement("div");
    row.className = "audit-item";
    const blocker = event.payload?.blocker_code ? ` | ${event.payload.blocker_code}` : "";
    row.textContent = `${event.event_type} | ${event.status}${blocker}`;
    els.outboxEvents.append(row);
  }
}

async function loadSettlements() {
  await ensureLogin();
  const data = await api().listSettlements();
  state.settlements = data.settlements || [];
  els.queueStatus.textContent = `${data.total || state.settlements.length} settlement items`;
  renderList();
}

async function loadSettlement(tripId) {
  state.selected = await api().getSettlement(tripId);
  renderList();
  renderDetail();
}

async function releaseSelected() {
  if (!state.selected) throw new Error("Select a settlement first");
  try {
    await api().releaseSettlement(state.selected.trip_id, {
      amount: state.selected.amount || 0,
      commission_amount: Math.round((state.selected.amount || 0) * 0.1),
      gst_amount: Math.round((state.selected.amount || 0) * 0.018),
      driver_payable_amount: Math.round((state.selected.amount || 0) * 0.9),
      currency: state.selected.currency || "INR",
      idempotency_key: `finance-console-${state.selected.trip_id}`,
      trace_id: `finance-console-${crypto.randomUUID()}`,
      confidence_score: 0.91,
      decision_reason: "Finance console settlement release preflight",
      evidence_refs: ["pod:verified", "otp:verified"]
    });
  } catch (error) {
    state.selected.blocker_code = blockerCodeFromError(error);
    state.selected.blocker_reason = error.payload?.detail?.message || error.payload?.detail || error.message;
    renderDetail();
    return;
  }
  await loadSettlement(state.selected.trip_id);
  await loadSettlements();
  await loadSettlement(state.selected.trip_id);
}

async function run(handler) {
  try {
    await handler();
  } catch (error) {
    window.alert(error.message || String(error));
  }
}

els.login.addEventListener("click", () => run(async () => { await login(); await loadSettlements(); }));
els.refresh.addEventListener("click", () => run(loadSettlements));
els.apiBase.addEventListener("change", () => run(loadSettlements));
els.role.addEventListener("change", () => { state.role = els.role.value; renderDetail(); });
els.releaseSettlement.addEventListener("click", () => run(releaseSelected));

loadSettlements();
