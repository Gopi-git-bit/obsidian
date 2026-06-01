// Generated from FastAPI OpenAPI. Do not edit by hand.

function buildUrl(baseUrl, path, query) {
  const url = new URL(path, baseUrl);
  for (const [key, value] of Object.entries(query || {})) {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  }
  return url;
}

async function request(baseUrl, path, options = {}) {
  const headers = { "content-type": "application/json" };
  if (options.token) headers.authorization = `Bearer ${options.token}`;
  const response = await fetch(buildUrl(baseUrl, path, options.query), { method: options.method || "GET", headers, body: options.body });
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

export class ZippyTransportCompanyApi {
  constructor(baseUrl, token = "") {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.token = token;
  }
  setToken(token) { this.token = token; }

  async devLogin(body, query = {}) {
    return request(this.baseUrl, `/api/v1/auth/dev-login`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async createVehicle(body, query = {}) {
    return request(this.baseUrl, `/api/v1/vehicles`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async listVehicles(query = {}) {
    return request(this.baseUrl, `/api/v1/vehicles`, { method: "GET", query, token: this.token });
  }
  async getVehicle(vehicle_id, query = {}) {
    return request(this.baseUrl, `/api/v1/vehicles/${vehicle_id}`, { method: "GET", query, token: this.token });
  }
  async updateVehicle(vehicle_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/vehicles/${vehicle_id}`, { method: "PATCH", query, token: this.token, body: JSON.stringify(body) });
  }
  async listMatches(query = {}) {
    return request(this.baseUrl, `/api/v1/matches`, { method: "GET", query, token: this.token });
  }
  async acceptMatch(match_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/matches/${match_id}/accept`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async rejectMatch(match_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/matches/${match_id}/reject`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async listTrips(query = {}) {
    return request(this.baseUrl, `/api/v1/transport-company/trips`, { method: "GET", query, token: this.token });
  }
  async getTrip(trip_id, query = {}) {
    return request(this.baseUrl, `/api/v1/transport-company/trips/${trip_id}`, { method: "GET", query, token: this.token });
  }
  async createQuote(order_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/orders/${order_id}/quote`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
  async releaseSettlement(trip_id, body, query = {}) {
    return request(this.baseUrl, `/api/v1/trips/${trip_id}/settlements/release`, { method: "POST", query, token: this.token, body: JSON.stringify(body) });
  }
}
