import { ZippyTransportCompanyApi } from "./api/generated-client.js";

const state = {
  api: null,
  token: sessionStorage.getItem("zippyTransportToken") || "",
  username: sessionStorage.getItem("zippyTransportUsername") || "transport-company-web-dev",
  vehicles: [],
  matches: [],
  trips: [],
  selected: null
};

const els = {
  apiBase: document.querySelector("#apiBase"),
  username: document.querySelector("#username"),
  login: document.querySelector("#login"),
  loginStatus: document.querySelector("#loginStatus"),
  addVehicle: document.querySelector("#addVehicle"),
  refresh: document.querySelector("#refresh"),
  vehicleStatus: document.querySelector("#vehicleStatus"),
  vehicleList: document.querySelector("#vehicleList"),
  matchStatus: document.querySelector("#matchStatus"),
  matchList: document.querySelector("#matchList"),
  emptyState: document.querySelector("#emptyState"),
  detail: document.querySelector("#detail"),
  detailTitle: document.querySelector("#detailTitle"),
  detailSub: document.querySelector("#detailSub"),
  detailBadge: document.querySelector("#detailBadge"),
  records: document.querySelector("#records"),
  acceptMatch: document.querySelector("#acceptMatch"),
  rejectMatch: document.querySelector("#rejectMatch")
};

els.username.value = state.username;

function api() {
  const baseUrl = els.apiBase.value.trim() || "http://127.0.0.1:8000";
  if (!state.api || state.api.baseUrl !== baseUrl.replace(/\/$/, "")) {
    state.api = new ZippyTransportCompanyApi(baseUrl, state.token);
  }
  state.api.setToken(state.token);
  return state.api;
}

function pretty(value) { return JSON.stringify(value, null, 2); }
function status(el, text) { el.textContent = text; }

async function login() {
  const username = els.username.value.trim() || "transport-company-web-dev";
  const data = await api().devLogin({ username, password: "transport-company-web-dev", role: "transport_company" });
  state.token = data.access_token;
  state.username = username;
  sessionStorage.setItem("zippyTransportToken", state.token);
  sessionStorage.setItem("zippyTransportUsername", username);
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

function renderVehicles() {
  els.vehicleList.innerHTML = "";
  for (const vehicle of state.vehicles) {
    const row = document.createElement("button");
    row.className = "row";
    row.type = "button";
    row.innerHTML = `<span class="row-main"><strong>${vehicle.manufacturer} ${vehicle.model_name}</strong><span>${vehicle.category}</span></span><span class="row-sub">${vehicle.id}</span>`;
    row.addEventListener("click", () => renderDetail("Vehicle", vehicle, vehicle.category));
    els.vehicleList.append(row);
  }
}

function renderMatches() {
  els.matchList.innerHTML = "";
  for (const match of state.matches) {
    const row = document.createElement("button");
    row.className = "row";
    row.type = "button";
    row.innerHTML = `<span class="row-main"><strong>Match ${match.id}</strong><span>${match.status}</span></span><span class="row-sub">Vehicle ${match.vehicle_id}</span>`;
    row.addEventListener("click", () => renderDetail("Match", match, match.status));
    els.matchList.append(row);
  }
  for (const item of state.trips) {
    const row = document.createElement("button");
    row.className = "row";
    row.type = "button";
    row.innerHTML = `<span class="row-main"><strong>${item.order.origin_city} -> ${item.order.destination_city}</strong><span>${item.trip.status}</span></span><span class="row-sub">Trip ${item.trip.trip_id}</span>`;
    row.addEventListener("click", () => renderDetail("Trip", item, item.trip.status));
    els.matchList.append(row);
  }
}

function record(title, value) {
  const card = document.createElement("div");
  card.className = "record-card";
  card.innerHTML = `<strong>${title}</strong><pre>${pretty(value)}</pre>`;
  els.records.append(card);
}

function renderDetail(kind, value, badge) {
  state.selected = { kind, value };
  els.emptyState.classList.add("hidden");
  els.detail.classList.remove("hidden");
  els.detailTitle.textContent = kind;
  els.detailSub.textContent = value.id || value.trip?.trip_id || value.vehicle_id || "";
  els.detailBadge.textContent = badge || "";
  els.records.innerHTML = "";
  record(kind, value);
  els.acceptMatch.disabled = kind !== "Match" || value.status !== "proposed";
  els.rejectMatch.disabled = kind !== "Match" || value.status !== "proposed";
}

async function loadAll() {
  await ensureLogin();
  const [vehicles, matches, trips] = await Promise.all([
    api().listVehicles({ limit: 100 }),
    api().listMatches({ limit: 100 }),
    api().listTrips()
  ]);
  state.vehicles = vehicles.vehicles || [];
  state.matches = matches.matches || [];
  state.trips = trips.trips || [];
  status(els.vehicleStatus, `${vehicles.total || state.vehicles.length} vehicles`);
  status(els.matchStatus, `${state.matches.length} matches, ${state.trips.length} trips`);
  renderVehicles();
  renderMatches();
}

async function run(handler) {
  try {
    await handler();
    await loadAll();
  } catch (error) {
    window.alert(error.message || String(error));
  }
}

els.login.addEventListener("click", () => run(async () => { await login(); }));
els.refresh.addEventListener("click", () => run(loadAll));
els.apiBase.addEventListener("change", () => run(loadAll));
els.addVehicle.addEventListener("click", () => run(async () => {
  await api().createVehicle({
    manufacturer: "Company Fleet",
    model_name: `Vehicle ${crypto.randomUUID().slice(0, 8)}`,
    category: "LCV",
    body_type: "open",
    gvw_kg: 3500,
    payload_kg: 2000,
    mileage_kmpl: 12,
    price_ex_showroom: 1200000
  });
}));
els.acceptMatch.addEventListener("click", () => run(async () => {
  await api().acceptMatch(state.selected.value.id, { notes: "accepted by company web" });
}));
els.rejectMatch.addEventListener("click", () => run(async () => {
  await api().rejectMatch(state.selected.value.id, { notes: "rejected by company web" });
}));

loadAll();
