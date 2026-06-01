// Generated from FastAPI OpenAPI. Do not edit by hand.

function buildUrl(baseUrl, path, query) {
  const url = new URL(path, baseUrl);
  for (const [key, value] of Object.entries(query || {})) {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, String(value));
    }
  }
  return url;
}

async function request(baseUrl, path, options = {}) {
  const headers = { "content-type": "application/json" };
  if (options.token) {
    headers.authorization = `Bearer ${options.token}`;
  }
  const response = await fetch(buildUrl(baseUrl, path, options.query), {
    method: options.method || "GET",
    headers,
    body: options.body
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : null;
  if (!response.ok) {
    const error = new Error(data?.detail?.message || data?.detail || response.statusText);
    error.status = response.status;
    error.payload = data;
    throw error;
  }
  return data;
}

export class ZippyDriverApi {
  constructor(baseUrl, token = "") {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.token = token;
  }

  setToken(token) {
    this.token = token;
  }

  async devLogin(body, query = {}) {
    return request(this.baseUrl, `/api/v1/auth/dev-login`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async listDriverTrips(query = {}) {
    return request(this.baseUrl, `/api/v1/driver/trips`, { method: "GET", query, token: this.token });
  }
  async getDriverTrip(trip_id, query = {}) {
    return request(this.baseUrl, `/api/v1/driver/trips/${trip_id}`, { method: "GET", query, token: this.token });
  }
  async acknowledgeTrip(trip_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/driver/trips/${trip_id}/acknowledge`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async recordTripMilestone(trip_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/trips/${trip_id}/milestones`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async uploadLoadingPhoto(trip_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/trips/${trip_id}/loading-photo`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async uploadPod(trip_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/trips/${trip_id}/pod`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async assignTripDriver(trip_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/trips/${trip_id}/assign-driver`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async releaseSettlement(trip_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/trips/${trip_id}/settlements/release`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async transitionOrder(order_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/orders/${order_id}/transition`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
}
