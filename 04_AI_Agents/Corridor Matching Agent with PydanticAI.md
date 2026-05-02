---
type: ai_agent
domain: matching
decision_value: High
status: draft
related_hubs:
  - "[[AI Agents Hub]]"
  - "[[Algorithms Hub]]"
  - "[[Fleet & Transport Hub]]"
tags:
  - ai-agent
  - matching
  - pydantic-ai
  - corridor
  - freight
actors:
  - Corridor Matching Agent
region:
  - India
created: 2026-04-30
updated: 2026-04-30
---

# Corridor Matching Agent with PydanticAI

## Purpose

Convert corridor-level matching rules into a typed agent contract that can safely recommend direct or triangular routing for freight requests without allowing free-form LLM output to bypass operational guardrails.

This note refines the external `pydantic ai.txt` continuation draft into a vault-ready implementation direction.

## What The External Draft Gets Right

- Uses typed request and recommendation models instead of unstructured text.
- Separates business rules into reliability, routing, cargo compatibility, pricing, and escalation.
- Treats lane lookup, triangle search, and route risk as tools rather than prompt-only reasoning.
- Pushes the agent toward auditable outputs that can feed OMS, TMS, and dashboards.

## Key Refinements Needed Before Adoption

### 1. Keep Hard Rules In Code, Not Only In The Prompt

The draft correctly lists business rules, but too much of the decision logic still depends on model obedience.

Refinement:

- enforce cargo and vehicle compatibility in deterministic Python before or after the LLM call
- enforce score thresholds and escalation rules in validators or orchestrator code
- use the LLM for tradeoff explanation and structured recommendation synthesis, not for core eligibility checks

### 2. Fix Identifier Consistency

The draft uses inconsistent lane identity shapes:

- `lookup_lane_reliability()` expects one lane ID
- `evaluate()` builds `origin:destination:cargo_type`
- SQL examples sometimes assume `origin:destination`

Refinement:

- define one canonical key format for all matching layers
- recommended pattern: `origin_city:destination_city:vehicle_type:cargo_type`
- keep analytical lane IDs and operational request IDs separate

### 3. Avoid Hidden Cross-Field Contradictions

The current schema allows combinations that should be impossible, such as:

- `route_type = "direct"` with a non-null triangle route
- `status = "approved"` on a blocked vehicle-cargo mismatch
- tight SLA recommendations on weak grade lanes without buffer

Refinement:

- add `@model_validator(mode="after")` checks on `MatchRecommendation`
- reject impossible combinations instead of silently accepting them

### 4. Make Triangle Logic Deterministic

The draft says:

- use triangle only if combined score is `>= 1.2x` direct lane
- cycle time `<= 48h`
- extra km `<= 30%` of direct distance

But the provided SQL and models do not contain enough fields to verify all of that safely.

Refinement:

- fetch direct distance explicitly
- fetch compatibility per leg explicitly
- compute triangle eligibility in deterministic code
- let the LLM explain why the selected triangle is best among already-eligible candidates

### 5. Separate Operational Risk From Narrative Risk

`check_route_risk()` returns a loose dict and handwritten note strings.

Refinement:

- replace free-form dict with a typed `RouteRiskAssessment`
- use normalized flags such as `monsoon_risk`, `port_cutoff_risk`, `border_delay_risk`, `ghat_section_risk`
- keep a separate human-readable summary field if needed

### 6. Tighten PydanticAI Claims To Match Reality

The draft includes a few statements that are directionally useful but should not be copied as guarantees without verifying against the exact PydanticAI version in use.

Examples to treat carefully:

- retry behavior details
- custom retry prompt options
- runtime dynamic schema patterns
- model provider examples

Refinement:

- document these as implementation options, not guaranteed built-ins
- verify exact API behavior against the version we actually run

### 7. Improve Tool Contract Design

Tool outputs should carry enough structure for deterministic guardrails and analytics reuse.

Refinement:

- return typed models from all tools
- avoid generic `dict` outputs
- include timestamps, data freshness, and source fields where operational decisions depend on recency

### 8. Add Confidence Discipline

`agent_confidence` is useful, but the draft treats it as a free scalar.

Refinement:

- define confidence from observable conditions
- lower confidence when data freshness is stale, triangle fit is marginal, or risk flags stack up
- never use confidence as an override for hard safety rules

## Recommended Agent Boundary

The Corridor Matching Agent should do the following:

- read shipment request context
- query lane reliability, return-load opportunity, and route risk
- synthesize a structured recommendation
- explain the selected path
- emit escalation when deterministic policy requires human review

It should not:

- directly assign a vehicle
- mutate OMS order state
- approve incompatible cargo-vehicle combinations
- invent missing lane or risk data

## Recommended Typed Models

Use the external draft as the base, but add these models:

```python
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional


class RouteRiskAssessment(BaseModel):
    risk_level: Literal["low", "medium", "high"]
    flags: list[str] = Field(default_factory=list)
    summary: str = ""
    data_freshness_hours: float = Field(ge=0)


class MatchRecommendation(BaseModel):
    status: Literal["approved", "pending_review", "blocked", "escalate"]
    route_type: Literal["direct", "triangular"]
    recommended_lane: str
    triangle_route: Optional[TriangleCandidate] = None
    sla_window_hours: float = Field(gt=0)
    pricing_premium_pct: float = Field(ge=0, le=45)
    required_carrier_tier: Literal["standard", "premium", "specialized"]
    risk_flags: list[str] = Field(default_factory=list)
    agent_confidence: float = Field(ge=0, le=1)
    reasoning: str

    @model_validator(mode="after")
    def validate_route_shape(self):
        if self.route_type == "direct" and self.triangle_route is not None:
            raise ValueError("triangle_route must be null for direct recommendations")
        if self.route_type == "triangular" and self.triangle_route is None:
            raise ValueError("triangle_route is required for triangular recommendations")
        return self
```

## Recommended Orchestration Pattern

```text
1. Validate request shape
2. Fetch direct lane reliability
3. Run deterministic cargo and vehicle compatibility checks
4. Fetch route risk assessment
5. If direct backhaul is weak, fetch triangle candidates
6. Deterministically filter triangle candidates by distance, cycle time, and leg compatibility
7. Invoke the LLM only on eligible options
8. Validate recommendation
9. Apply final policy gate before dispatch or escalation
```

## Policy Gates That Should Be Deterministic

- lane score below minimum threshold
- reefer-required cargo matched to non-reefer vehicle
- low-bed-required cargo matched to standard body vehicle
- time-sensitive request on weak lane without allowed buffer
- port cutoff or compliance risk above configured threshold
- missing or stale lane data

## Suggested Integration With Existing Vault Work

This note should connect to:

- [[IMS Matching Engine]]
- [[Hub-Aware Return Trip Matching]]
- [[Triangle Route Engine for Return Trip Optimization]]
- [[Lane Reliability Scorecard for Return Trip Promise Engine]]
- [[Route Risk Scoring]]
- [[Transportation Agent]]
- [[Zippy Logistics Analytics Star Schema]]

## Practical Next Step

If this agent is implemented, create two follow-up artifacts:

- a matching policy note in `05_Algorithms/Matching` for deterministic rules
- a schema and event note in `10_Data_Model/Docs` for tool inputs, outputs, and audit events

That split will keep agent behavior, algorithm policy, and analytics lineage clean.
