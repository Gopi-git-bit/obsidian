import { ZippySupervisorApi } from "./api/generated-client.js";

const state = {
  api: null,
  token: sessionStorage.getItem("zippySupervisorToken") || "",
  username: sessionStorage.getItem("zippySupervisorUsername") || "supervisor-console-dev",
  cases: [],
  selected: null
};

const els = {
  apiBase: document.querySelector("#apiBase"),
  username: document.querySelector("#username"),
  login: document.querySelector("#login"),
  loginStatus: document.querySelector("#loginStatus"),
  refresh: document.querySelector("#refresh"),
  caseStatus: document.querySelector("#caseStatus"),
  caseList: document.querySelector("#caseList"),
  emptyState: document.querySelector("#emptyState"),
  caseDetail: document.querySelector("#caseDetail"),
  detailTitle: document.querySelector("#detailTitle"),
  detailSub: document.querySelector("#detailSub"),
  caseBadge: document.querySelector("#caseBadge"),
  records: document.querySelector("#records"),
  auditTrail: document.querySelector("#auditTrail"),
  holdCase: document.querySelector("#holdCase"),
  approveCase: document.querySelector("#approveCase"),
  rejectCase: document.querySelector("#rejectCase")
};

els.username.value = state.username;

function api() {
  const baseUrl = els.apiBase.value.trim() || "http://127.0.0.1:8000";
  if (!state.api || state.api.baseUrl !== baseUrl.replace(/\/$/, "")) {
    state.api = new ZippySupervisorApi(baseUrl, state.token);
  }
  state.api.setToken(state.token);
  return state.api;
}

function pretty(value) { return JSON.stringify(value, null, 2); }

async function login() {
  const username = els.username.value.trim() || "supervisor-console-dev";
  const data = await api().devLogin({ username, password: "supervisor-console-dev", role: "supervisor" });
  state.token = data.access_token;
  state.username = username;
  sessionStorage.setItem("zippySupervisorToken", state.token);
  sessionStorage.setItem("zippySupervisorUsername", username);
  api().setToken(state.token);
  els.loginStatus.textContent = `Signed in as ${data.username}`;
}

async function ensureLogin() {
  if (state.token) {
    els.loginStatus.textContent = `Signed in as ${state.username}`;
    return;
  }
  await login();
}

function renderCases() {
  els.caseList.innerHTML = "";
  for (const item of state.cases) {
    const c = item.case;
    const row = document.createElement("button");
    row.className = `row${state.selected?.case?.case_id === c.case_id ? " active" : ""}`;
    row.type = "button";
    row.innerHTML = `<span class="row-main"><strong>${c.title}</strong><span>${c.status}</span></span><span class="row-sub">${c.case_type} | ${c.case_id}</span>`;
    row.addEventListener("click", () => loadCase(c.case_id));
    els.caseList.append(row);
  }
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
  els.caseDetail.classList.toggle("hidden", !item);
  if (!item) return;
  els.detailTitle.textContent = `Case ${item.case.case_id}`;
  els.detailSub.textContent = `${item.case.case_type} | order ${item.case.order_id || "-"}`;
  els.caseBadge.textContent = item.case.status;
  els.records.innerHTML = "";
  card("Case", item.case);
  card("POD / OTP / Evidence", item.case.payload || {});
  card("Fraud Holds", item.fraud_holds || []);
  card("Settlement Holds", item.settlement_holds || []);
  els.auditTrail.innerHTML = "";
  for (const audit of item.audit_trail || []) {
    const row = document.createElement("div");
    row.className = "audit-item";
    row.textContent = `${audit.decision} by ${audit.decided_by} | ${audit.notes || ""}`;
    els.auditTrail.append(row);
  }
}

async function loadCases() {
  await ensureLogin();
  const data = await api().listCases();
  state.cases = data.cases || [];
  els.caseStatus.textContent = `${data.total || state.cases.length} cases`;
  renderCases();
}

async function loadCase(caseId) {
  state.selected = await api().getCase(caseId);
  renderCases();
  renderDetail();
}

async function run(handler) {
  try {
    await handler();
  } catch (error) {
    window.alert(error.message || String(error));
  }
}

async function decision(method) {
  if (!state.selected) throw new Error("Select a case first");
  const data = await method(state.selected.case.case_id, { reason: "Supervisor console action", notes: "Reviewed in console", payload: { source: "supervisor-console" } });
  state.selected = data;
  await loadCases();
  renderDetail();
}

els.login.addEventListener("click", () => run(async () => { await login(); await loadCases(); }));
els.refresh.addEventListener("click", () => run(loadCases));
els.apiBase.addEventListener("change", () => run(loadCases));
els.holdCase.addEventListener("click", () => run(() => decision(api().holdCase.bind(api()))));
els.approveCase.addEventListener("click", () => run(() => decision(api().approveCase.bind(api()))));
els.rejectCase.addEventListener("click", () => run(() => decision(api().rejectCase.bind(api()))));

loadCases();
