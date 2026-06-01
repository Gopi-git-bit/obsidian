import { ZippyCustomerApi } from "./api/generated-client.js";

const state = {
  api: null,
  token: sessionStorage.getItem("zippyCustomerToken") || "",
  username: sessionStorage.getItem("zippyCustomerUsername") || "customer-web-dev",
  orders: [],
  selectedOrder: null,
  flow: null
};

const els = {
  apiBase: document.querySelector("#apiBase"),
  username: document.querySelector("#username"),
  login: document.querySelector("#login"),
  loginStatus: document.querySelector("#loginStatus"),
  orderForm: document.querySelector("#orderForm"),
  refreshOrders: document.querySelector("#refreshOrders"),
  ordersStatus: document.querySelector("#ordersStatus"),
  ordersList: document.querySelector("#ordersList"),
  emptyState: document.querySelector("#emptyState"),
  orderDetail: document.querySelector("#orderDetail"),
  detailTitle: document.querySelector("#detailTitle"),
  detailRoute: document.querySelector("#detailRoute"),
  lifecycleBadge: document.querySelector("#lifecycleBadge"),
  flowSections: document.querySelector("#flowSections")
};

els.username.value = state.username;

function api() {
  const baseUrl = els.apiBase.value.trim() || "http://127.0.0.1:8000";
  if (!state.api || state.api.baseUrl !== baseUrl.replace(/\/$/, "")) {
    state.api = new ZippyCustomerApi(baseUrl, state.token);
  }
  state.api.setToken(state.token);
  return state.api;
}

function pretty(value) {
  return JSON.stringify(value, null, 2);
}

function orderLabel(order) {
  return `${order.origin_city} -> ${order.destination_city}`;
}

function setLoginStatus(message) {
  els.loginStatus.textContent = message;
}

function setStatus(message) {
  els.ordersStatus.textContent = message;
}

async function login() {
  const username = els.username.value.trim() || "customer-web-dev";
  const data = await api().devLogin({
    username,
    password: "customer-web-dev",
    role: "customer"
  });
  state.token = data.access_token;
  state.username = username;
  sessionStorage.setItem("zippyCustomerToken", state.token);
  sessionStorage.setItem("zippyCustomerUsername", username);
  api().setToken(state.token);
  setLoginStatus(`Signed in as ${data.username}`);
}

async function ensureLogin() {
  if (state.token) {
    setLoginStatus(`Signed in as ${state.username}`);
    return;
  }
  await login();
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

function addFlowSection(title, value) {
  const card = document.createElement("div");
  card.className = "record-card";
  card.innerHTML = `<strong>${title}</strong><pre>${pretty(value)}</pre>`;
  els.flowSections.append(card);
}

function renderFlow() {
  els.flowSections.innerHTML = "";
  const flow = state.flow || {};
  addFlowSection("Quote", flow.quote_records || []);
  addFlowSection("Match / Trip", {
    match_status: flow.match_status || [],
    trip_status: flow.trip_status || null
  });
  addFlowSection("Milestone", flow.milestone_status || []);
  addFlowSection("POD", flow.pod_status || {});
  addFlowSection("OTP", flow.otp_status || {});
  addFlowSection("Settlement / Invoice", {
    settlement_visibility: flow.settlement_visibility || [],
    invoice_visibility: flow.invoice_visibility || []
  });
}

function renderDetail() {
  const order = state.selectedOrder;
  els.emptyState.classList.toggle("hidden", Boolean(order));
  els.orderDetail.classList.toggle("hidden", !order);
  if (!order) return;

  els.detailTitle.textContent = `Order ${order.id}`;
  els.detailRoute.textContent = `${order.shipper_name} | ${orderLabel(order)} | ${order.weight_kg} kg`;
  els.lifecycleBadge.textContent = order.current_state;
  renderFlow();
}

async function loadOrders() {
  setStatus("Loading orders...");
  try {
    await ensureLogin();
    const data = await api().listOrders({ limit: 100 });
    state.orders = data.orders || [];
    setStatus(`${data.total || state.orders.length} orders`);
    renderOrders();
  } catch (error) {
    setStatus(`Could not load orders: ${error.message}`);
  }
}

async function loadOrder(orderId) {
  const [order, flow] = await Promise.all([
    api().getOrder(orderId),
    api().getCustomerFlowSummary(orderId)
  ]);
  state.selectedOrder = order;
  state.flow = flow;
  renderOrders();
  renderDetail();
}

function formPayload(form) {
  const data = new FormData(form);
  return {
    shipper_name: data.get("shipper_name"),
    shipper_phone: data.get("shipper_phone"),
    shipper_email: data.get("shipper_email"),
    origin_city: data.get("origin_city"),
    origin_state: data.get("origin_state"),
    destination_city: data.get("destination_city"),
    destination_state: data.get("destination_state"),
    cargo_type: "general",
    weight_kg: Number(data.get("weight_kg")),
    num_packages: Number(data.get("num_packages")),
    vehicle_category_preference: data.get("vehicle_category_preference") || null,
    is_interstate: false,
    estimated_distance_km: Number(data.get("estimated_distance_km")),
    offered_price: Number(data.get("offered_price"))
  };
}

els.login.addEventListener("click", async () => {
  try {
    await login();
    await loadOrders();
  } catch (error) {
    window.alert(error.message || String(error));
  }
});

els.refreshOrders.addEventListener("click", loadOrders);
els.apiBase.addEventListener("change", loadOrders);

els.orderForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await ensureLogin();
    const order = await api().createOrder(formPayload(els.orderForm));
    await loadOrders();
    await loadOrder(order.id);
  } catch (error) {
    window.alert(error.message || String(error));
  }
});

loadOrders();
