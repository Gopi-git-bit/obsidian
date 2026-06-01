// Generated from FastAPI OpenAPI. Do not edit by hand.

export interface AdvancePaymentRequest {
  idempotency_key: string;
  amount: number;
  currency?: string;
  provider_ref?: string | unknown;
}

export interface BidCounter {
  counter_amount: number;
  notes?: string | unknown;
}

export interface BidCreate {
  vehicle_id: string;
  driver_name: string;
  driver_phone: string;
  bid_amount: number;
  estimated_eta_hours?: number | unknown;
  estimated_arrival_hours?: number | unknown;
  vehicle_available_at?: string | unknown;
  notes?: string | unknown;
}

export interface BidListResponse {
  total: number;
  bids: Array<BidResponse>;
}

export interface BidResponse {
  id: string;
  order_id: string;
  vehicle_id: string;
  driver_name: string;
  driver_phone: string;
  bid_amount: number;
  counter_amount: number | unknown;
  estimated_eta_hours: number | unknown;
  estimated_arrival_hours: number | unknown;
  vehicle_available_at: string | unknown;
  notes: string | unknown;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Body_optimize_multi_stop_api_v1_optimize_multi_stop_post {
  origin: RouteNodeInput;
  destinations: Array<RouteNodeInput>;
  vehicle: RouteVehicleInput;
}

export interface DevLoginRequest {
  username: string;
  password: string;
  role?: unknown;
}

export interface DriverAssignRequest {
  driver_id: string;
}

export interface HTTPValidationError {
  detail?: Array<ValidationError>;
}

export interface HealthResponse {
  status: string;
  database: string;
  version: string;
}

export interface JournalLine {
  debit_ledger?: string | unknown;
  credit_ledger?: string | unknown;
  amount: number;
}

export interface LoadingPhotoRequest {
  idempotency_key: string;
  photo_url: string;
  uploaded_by: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface MLPricingRequest {
  weight_kg: number;
  distance_km: number;
  vehicle_category?: string;
  origin_city?: string;
  destination_city?: string;
  is_interstate?: boolean;
  is_festival?: boolean;
  is_remote?: boolean;
  is_hill?: boolean;
  is_congested?: boolean;
  service_type?: string;
  customer_type?: string;
  demand?: number;
  supply?: number;
  diesel_price?: number;
  route_difficulty_score?: number | unknown;
  lane_viability?: string | unknown;
  return_load_probability?: number | unknown;
}

export interface MLPricingResponse {
  base_cost: number;
  base_rate_per_km: number;
  city_tier: number;
  tier_multiplier: number;
  fuel_index: number;
  tier_adjusted_cost: number;
  route_difficulty: Record<string, unknown>;
  urbanization_density: Record<string, unknown>;
  surcharges: Record<string, unknown>;
  total_surcharge_pct: number;
  surcharge_amount: number;
  density_adjusted_cost: number;
  surge_multiplier: number;
  surge_model: string;
  surge_confidence: number;
  surge_amount: number;
  service_type: string;
  service_multiplier: number;
  service_amount: number;
  deadhead_lane_viability: Record<string, unknown>;
  deadhead_amount: number;
  subtotal: number;
  customer_type: string;
  customer_adjustment: number;
  platform_fee_pct: number;
  platform_fee: number;
  gst_breakdown: Record<string, unknown>;
  gst_amount: number;
  savings_vs_broker_pct: number;
  final_price: number;
  currency?: string;
  breakdown_per_km: number;
}

export interface MatchAction {
  notes?: string | unknown;
}

export interface MatchListResponse {
  total: number;
  matches: Array<MatchResponse>;
}

export interface MatchResponse {
  id: string;
  order_id: string;
  vehicle_id: string;
  bid_id: string | unknown;
  match_score: number | unknown;
  utilization_percent: number | unknown;
  efficiency_score: number | unknown;
  agreed_price: number | unknown;
  platform_fee: number | unknown;
  gst_amount: number | unknown;
  total_amount: number | unknown;
  status: string;
  matched_at: string | unknown;
  accepted_at: string | unknown;
  completed_at: string | unknown;
  created_at: string;
}

export interface MilestoneRequest {
  idempotency_key: string;
  milestone_type: string;
  status?: string;
  payload?: Record<string, unknown>;
}

export interface OTPVerifyRequest {
  idempotency_key: string;
  otp: string;
  verified_by: string;
}

export interface OptimizeRouteRequest {
  nodes: Array<RouteNodeInput>;
  vehicles: Array<RouteVehicleInput>;
  optimize_for?: string;
  time_limit_seconds?: number;
  use_drl?: boolean;
}

export interface OptimizeRouteResponse {
  order_id: string;
  routes: Array<unknown>;
  total_distance_km: number;
  total_duration_min: number;
  total_cost: number;
  model_used: string;
  confidence: number;
  fallback_reason?: string | unknown;
  solve_time_ms: number;
}

export interface OrderCreate {
  customer_id?: string | unknown;
  vehicle_id?: string | unknown;
  shipper_name: string;
  shipper_phone: string;
  shipper_email?: string | unknown;
  origin_city: string;
  origin_state: string;
  origin_pincode?: string | unknown;
  origin_lat?: number | unknown;
  origin_lng?: number | unknown;
  destination_city: string;
  destination_state: string;
  destination_pincode?: string | unknown;
  destination_lat?: number | unknown;
  destination_lng?: number | unknown;
  cargo_type?: string;
  cargo_description?: string | unknown;
  material_type?: string;
  body_type_required?: string;
  payment_mode?: string;
  topay_consent_status?: string;
  weight_kg: number;
  volume_cbm?: number | unknown;
  num_packages?: number;
  vehicle_category_preference?: string | unknown;
  is_interstate?: boolean;
  is_festival_period?: boolean;
  is_remote_location?: boolean;
  is_hill_area?: boolean;
  estimated_distance_km?: number | unknown;
  estimated_duration_hours?: number | unknown;
  offered_price?: number | unknown;
  pickup_datetime?: string | unknown;
  delivery_deadline?: string | unknown;
  payload_metadata?: Record<string, unknown>;
  notes?: string | unknown;
}

export interface OrderIntakeRequest {
  shipper_name: string;
  shipper_phone: string;
  shipper_email?: string | unknown;
  origin_city: string;
  origin_state: string;
  origin_pincode?: string | unknown;
  origin_lat?: number | unknown;
  origin_lng?: number | unknown;
  destination_city: string;
  destination_state: string;
  destination_pincode?: string | unknown;
  destination_lat?: number | unknown;
  destination_lng?: number | unknown;
  cargo_type?: string;
  cargo_description?: string | unknown;
  weight_kg: number;
  volume_cbm?: number | unknown;
  num_packages?: number;
  vehicle_category_preference?: string | unknown;
  is_interstate?: boolean;
  estimated_distance_km?: number | unknown;
  estimated_duration_hours?: number | unknown;
  offered_price?: number | unknown;
  pickup_datetime?: string | unknown;
  delivery_deadline?: string | unknown;
  consent_id: string;
  privacy_notice_version: string;
  idempotency_key: string;
  notes?: string | unknown;
}

export interface OrderIntakeResponse {
  order_id: string;
  status: string;
  shipper_name: string;
  shipper_phone: string;
  origin_city: string;
  destination_city: string;
  consent_id: string;
  privacy_notice_version: string;
  idempotency_key: string;
  created_at: string;
}

export interface OrderListResponse {
  total: number;
  limit: number;
  offset: number;
  orders: Array<OrderResponse>;
}

export interface OrderResponse {
  id: string;
  customer_id: string | unknown;
  vehicle_id: string | unknown;
  shipper_name: string;
  shipper_phone: string;
  shipper_email: string | unknown;
  origin_city: string;
  origin_state: string;
  origin_pincode: string | unknown;
  origin_lat: number | unknown;
  origin_lng: number | unknown;
  destination_city: string;
  destination_state: string;
  destination_pincode: string | unknown;
  destination_lat: number | unknown;
  destination_lng: number | unknown;
  cargo_type: string;
  cargo_description: string | unknown;
  material_type: string;
  body_type_required: string;
  payment_mode: string;
  topay_consent_status: string;
  weight_kg: number;
  volume_cbm: number | unknown;
  num_packages: number;
  vehicle_category_preference: string | unknown;
  is_interstate: boolean;
  is_festival_period: boolean;
  is_remote_location: boolean;
  is_hill_area: boolean;
  estimated_distance_km: number | unknown;
  estimated_duration_hours: number | unknown;
  offered_price: number | unknown;
  negotiated_price: number | unknown;
  pickup_datetime: string | unknown;
  delivery_deadline: string | unknown;
  current_state: string;
  status: string;
  payload_metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface OrderStateEventListResponse {
  total: number;
  events: Array<StateAuditLogResponse>;
}

export interface OrderTransitionRequest {
  to_state: string;
  event: string;
  payload: Record<string, unknown>;
  actor_role: string;
  actor_id?: string | unknown;
  idempotency_key: string;
  trace_id: string;
  reason?: string | unknown;
  evidence_ref?: string | unknown;
}

export interface OrderUpdate {
  offered_price?: number | unknown;
  negotiated_price?: number | unknown;
  notes?: string | unknown;
}

export interface PODUploadRequest {
  idempotency_key: string;
  pod_url: string;
  consignee_otp: string;
  pod_exif?: Record<string, unknown>;
  uploaded_by: string;
}

export interface PODVerifyRequest {
  idempotency_key: string;
  verified_by: string;
}

export interface PerformanceObligationEvidence {
  vehicle_assigned: boolean;
  trip_completed: boolean;
  pod_uploaded: boolean;
  pod_verified: boolean;
  otp_verified: boolean;
  cancellation_hold?: boolean;
  fraud_hold?: boolean;
  dispute_hold?: boolean;
  claim_hold?: boolean;
  completed_at?: string | unknown;
}

export interface PriceEstimateRequest {
  weight_kg: number;
  distance_km: number;
  vehicle_category?: string | unknown;
  is_interstate?: boolean;
  is_festival_period?: boolean;
  is_remote_location?: boolean;
  is_hill_area?: boolean;
  is_congested_route?: boolean;
}

export interface PriceEstimateResponse {
  base_cost: number;
  distance_rate: number;
  surcharges: Record<string, unknown>;
  platform_fee: number;
  gst_amount: number;
  total_amount: number;
  currency?: string;
}

export interface RevenueRecognitionRequest {
  order_id: string;
  user_id: string;
  invoice_generation_user_id: string;
  invoice_approval_user_id: string;
  principal_agent_status?: string;
  revenue_presentation?: string;
  gross_freight_amount: number;
  driver_payable_amount: number;
  commission_amount: number;
  platform_fee_amount?: number;
  gst_amount?: number;
  revenue_amount?: number | unknown;
  accounting_policy_version: string;
  idempotency_key: string;
  performance_obligation: PerformanceObligationEvidence;
}

export interface RevenueRecognitionResponse {
  order_id: string;
  recognition_status: string;
  recognized_at: string;
  principal_agent_status: string;
  revenue_presentation: string;
  revenue_amount: number;
  gst_amount: number;
  accounting_policy_version: string;
  idempotency_key: string;
  journal_lines: Array<JournalLine>;
}

export interface RouteNodeInput {
  id: string;
  lat: number;
  lng: number;
  demand_kg?: number;
  time_window_start?: number;
  time_window_end?: number;
  service_time_min?: number;
  is_depot?: boolean;
}

export interface RouteVehicleInput {
  id: string;
  capacity_kg?: number;
  cost_per_km?: number;
  max_distance_km?: number;
  max_stops?: number;
}

export interface SettlementReleaseRequest {
  idempotency_key: string;
  amount: number;
  commission_amount: number;
  gst_amount: number;
  driver_payable_amount: number;
  currency?: string;
}

export interface ShipmentStatusListResponse {
  total: number;
  shipments: Array<ShipmentStatusResponse>;
}

export interface ShipmentStatusResponse {
  order_id: string;
  shipment_status: string;
  origin_city: string;
  destination_city: string;
  latest_milestone: string;
  delay_risk: string;
  current_eta: string | unknown;
  customer_phone: string | unknown;
  updated_at: string;
}

export interface StateAuditLogResponse {
  log_id: string;
  order_id: string;
  from_state: string;
  to_state: string;
  event_name: string;
  actor_role: string;
  actor_id: string | unknown;
  idempotency_key: string;
  trace_id: string;
  payload_hash: string;
  timestamp: string;
}

export interface SurgePredictRequest {
  demand?: number;
  supply?: number;
  city?: string;
  is_remote?: boolean;
  is_hill?: boolean;
  is_festival?: boolean;
  distance_km?: number;
  origin_city?: string;
  destination_city?: string;
  congestion_level?: number;
  vehicle_category?: string;
  vehicle_age?: number;
  diesel_price?: number;
  customer_type?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type?: string;
  role: UserRole;
  username: string;
}

export interface TripAcknowledgeRequest {
  idempotency_key: string;
  acknowledged_by?: string | unknown;
}

export interface ValidationError {
  loc: Array<string | number>;
  msg: string;
  type: string;
}

export interface VehicleListResponse {
  total: number;
  limit: number;
  offset: number;
  vehicles: Array<VehicleResponse>;
}

export interface VehicleRecommendResponse {
  vehicle: VehicleResponse;
  utilization_percent: number;
  efficiency_score: number;
  recommended?: boolean;
}

export interface VehicleResponse {
  id: string;
  manufacturer: string;
  model_name: string;
  variant: string | unknown;
  category: string;
  body_type: string;
  gvw_kg: number | unknown;
  payload_kg: number | unknown;
  tonnage_class: string | unknown;
  length_mm: number | unknown;
  width_mm: number | unknown;
  height_mm: number | unknown;
  wheelbase_mm: number | unknown;
  loading_length_mm: number | unknown;
  loading_width_mm: number | unknown;
  loading_height_mm: number | unknown;
  engine_cc: number | unknown;
  engine_cylinders: number | unknown;
  power_hp: number | unknown;
  torque_nm: number | unknown;
  fuel_tank_ltr: number | unknown;
  mileage_kmpl: number | unknown;
  emission_norm: string | unknown;
  axle_config: string | unknown;
  tyres: number | unknown;
  price_ex_showroom: number | unknown;
}
