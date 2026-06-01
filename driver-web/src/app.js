import { ZippyDriverApi } from "./api/generated-client.js";

const state = {
  api: null,
  token: sessionStorage.getItem("zippyDriverToken") || "",
  username: sessionStorage.getItem("zippyDriverUsername") || "driver-web-dev",
  trips: [],
  selectedTrip: null
};

const els = {
  apiBase: document.querySelector("#apiBase"),
  username: document.querySelector("#username"),
  login: document.querySelector("#login"),
  loginStatus: document.querySelector("#loginStatus"),
  refreshTrips: document.querySelector("#refreshTrips"),
  tripsStatus: document.querySelector("#tripsStatus"),
  tripsList: document.querySelector("#tripsList"),
  emptyState: document.querySelector("#emptyState"),
  tripDetail: document.querySelector("#tripDetail"),
  detailTitle: document.querySelector("#detailTitle"),
  detailRoute: document.querySelector("#detailRoute"),
  tripBadge: document.querySelector("#tripBadge"),
  recordSections: document.querySelector("#recordSections"),
  ackTrip: document.querySelector("#ackTrip"),
  addMilestone: document.querySelector("#addMilestone"),
  uploadLoading: document.querySelector("#uploadLoading"),
  uploadPod: document.querySelector("#uploadPod")
};

els.username.value = state.username;

function api() {
  const baseUrl = els.apiBase.value.trim() || "http://127.0.0.1:8000";
  if (!state.api || state.api.baseUrl !== baseUrl.replace(/\/$/, "")) {
    state.api = new ZippyDriverApi(baseUrl, state.token);
  }
  state.api.setToken(state.token);
  return state.api;
}

function pretty(value) {
  return JSON.stringify(value, null, 2);
}

function routeLabel(item) {
  const order = item.order || {};
  return `${order.origin_city || "-"} -> ${order.destination_city || "-"}`;
}

function setLoginStatus(message) {
  els.loginStatus.textContent = message;
}

function setStatus(message) {
  els.tripsStatus.textContent = message;
}

async function login() {
  const username = els.username.value.trim() || "driver-web-dev";
  const data = await api().devLogin({
    username,
    password: "driver-web-dev",
    role: "driver"
  });
  state.token = data.access_token;
  state.username = username;
  sessionStorage.setItem("zippyDriverToken", state.token);
  sessionStorage.setItem("zippyDriverUsername", username);
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

function renderTrips() {
  els.tripsList.innerHTML = "";
  for (const item of state.trips) {
    const row = document.createElement("button");
    row.type = "button";
    row.className = `trip-row${state.selectedTrip?.trip?.trip_id === item.trip.trip_id ? " active" : ""}`;
    row.innerHTML = `
      <span class="row-main">
        <strong>${routeLabel(item)}</strong>
        <span>${item.trip.status}</span>
      </span>
      <span class="row-sub">${item.order.current_state}</span>
      <span class="row-sub">${item.trip.trip_id}</span>
    `;
    row.addEventListener("click", () => loadTrip(item.trip.trip_id));
    els.tripsList.append(row);
  }
}

function addRecordSection(title, value) {
  const card = document.createElement("div");
  card.className = "record-card";
  card.innerHTML = `<strong>${title}</strong><pre>${pretty(value)}</pre>`;
  els.recordSections.append(card);
}

function renderDetail() {
  const item = state.selectedTrip;
  els.emptyState.classList.toggle("hidden", Boolean(item));
  els.tripDetail.classList.toggle("hidden", !item);
  if (!item) return;

  els.detailTitle.textContent = `Trip ${item.trip.trip_id}`;
  els.detailRoute.textContent = `${routeLabel(item)} | ${item.order.weight_kg} kg | ${item.order.num_packages} packages`;
  els.tripBadge.textContent = item.trip.status;
  els.recordSections.innerHTML = "";
  addRecordSection("Order Route / Status", item.order);
  addRecordSection("Assigned Vehicle / Match", {
    vehicle_id: item.trip.vehicle_id,
    match: item.match
  });
  addRecordSection("Milestones", item.milestones || []);
  addRecordSection("Loading Proof", item.loading_proofs || []);
  addRecordSection("POD Status", item.pod_status || {});
  addRecordSection("OTP Status", item.otp_status || {});
}

async function loadTrips() {
  setStatus("Loading trips...");
  try {
    await ensureLogin();
    const data = await api().listDriverTrips();
    state.trips = data.trips || [];
    setStatus(`${data.total || state.trips.length} trips`);
    renderTrips();
  } catch (error) {
    setStatus(`Could not load trips: ${error.message}`);
  }
}

async function loadTrip(tripId) {
  state.selectedTrip = await api().getDriverTrip(tripId);
  renderTrips();
  renderDetail();
}

async function runTripAction(handler) {
  try {
    if (!state.selectedTrip) throw new Error("Select a trip first");
    await handler(state.selectedTrip.trip.trip_id);
    await loadTrip(state.selectedTrip.trip.trip_id);
    await loadTrips();
  } catch (error) {
    window.alert(error.message || String(error));
  }
}

els.login.addEventListener("click", async () => {
  try {
    await login();
    await loadTrips();
  } catch (error) {
    window.alert(error.message || String(error));
  }
});

els.refreshTrips.addEventListener("click", loadTrips);
els.apiBase.addEventListener("change", loadTrips);

els.ackTrip.addEventListener("click", () => runTripAction((tripId) => api().acknowledgeTrip(tripId, {
  acknowledged_by: state.username,
  idempotency_key: `ack-${crypto.randomUUID()}`
})));

els.addMilestone.addEventListener("click", () => runTripAction((tripId) => api().recordTripMilestone(tripId, {
  milestone_type: "in_transit",
  status: "recorded",
  payload: {},
  idempotency_key: `driver-mile-${crypto.randomUUID()}`
})));

els.uploadLoading.addEventListener("click", () => runTripAction((tripId) => api().uploadLoadingPhoto(tripId, {
  photo_url: "s3://docs/driver-loading.jpg",
  uploaded_by: state.username,
  idempotency_key: `driver-loading-${crypto.randomUUID()}`
})));

els.uploadPod.addEventListener("click", () => runTripAction((tripId) => api().uploadPod(tripId, {
  pod_url: "s3://docs/driver-pod.jpg",
  consignee_otp: "123456",
  pod_exif: {},
  uploaded_by: state.username,
  idempotency_key: `driver-pod-${crypto.randomUUID()}`
})));

loadTrips();
