---
type: memo
domain: product
scope: distillation
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Operations Strategy Hub]]"
  - "[[Technology Stack Hub]]"
  - "[[Business Models Hub]]"
tags:
  - prd
  - product
  - architecture
  - distillation
---

# Master PRD Distillation for Current Project

## Purpose

This note extracts only the durable, project-relevant parts of the older `master prd.txt`.

It intentionally ignores:

- outdated framework selections
- model-specific AI assignments
- deployment and infra choices that may change

## High-Value Parts That Still Fit

## 1. Multi-Surface Product Shape

The older PRD is still correct that the platform needs multiple operational surfaces:

- customer-facing booking and tracking flows
- driver-facing execution and POD flows
- transport-company-facing fleet and provider workflows
- admin and ops oversight flows

That matches the current project well.

## 2. Backend As The Coordination Core

The most durable architectural idea in the old PRD is that the backend is the coordination layer between:

- order creation
- matching
- trip execution
- pricing
- payment
- notifications
- analytics

That still fits the current project exactly.

## 3. Realtime Operational Updates

The specific transport may change, but the product still needs realtime behavior for:

- order status changes
- driver and trip tracking
- assignment changes
- delay and alert events
- payment confirmations

The mechanism can change. The requirement itself is durable.

## 4. Payments, Maps, Notifications, And File Handling As Core Integrations

The exact vendor can change, but the project still needs backend support for:

- payment processing
- routing and distance computation
- geocoding and location storage
- notifications
- document and POD storage

These are product requirements, not stack preferences.

## 5. Testing As A First-Class Backend Concern

The old PRD correctly emphasized that the backend must be testable across:

- API workflows
- pricing logic
- route and distance logic
- payments and refunds
- role-based permissions
- end-to-end order execution

That aligns well with the current project direction.

## What Has Drifted And Should Not Be Treated As Current Truth

## 1. Django-Centered Backend Assumption

The current repo is FastAPI-based, so the old Django-first stack should not be treated as the present architecture.

## 2. Specific AI Model Assignments

Those are unstable and should not be used as the source of truth for current design.

## 3. Full Tech Stack Prescription

The old PRD bundled:

- frontend frameworks
- backend frameworks
- workflow tools
- cloud tools
- observability stack
- testing stack

Useful historically, but too volatile to anchor the current documentation.

## Current-Project Interpretation

The older master PRD is best treated as a broad capability checklist, not as the current implementation guide.

Its durable contribution is this product structure:

```text
multi-role logistics platform
-> backend coordination core
-> operational workflows
-> realtime visibility
-> pricing, payment, and routing support
-> analytics feedback loop
```

## How It Maps To Current Project Notes

| Old PRD Theme | Current Note |
|---|---|
| Backend coordination core | [[Backend Structure for Current Project]] |
| Operational database shape | [[Zippy Logistics Operational Core Schema]] |
| SLA and delivery promise logic | [[On-Time Delivery Control Tower Strategy for Multimodal Freight]] |
| Pricing and market signals | `10_Data_Model` pricing tables + pricing notes |
| Partner and provider model | [[Transport Company Network Model]] |

## Recommended Use Of The Old Master PRD

Use it only for:

- checking whether a capability area was forgotten
- validating that the platform still supports all main user surfaces
- reminding the team that payments, routing, notifications, and files are all first-class backend concerns

Do not use it for:

- choosing the current backend framework
- choosing AI model providers
- deciding cloud or deployment architecture
- treating every listed tool as mandatory

## Bottom Line

The old master PRD is still useful, but only after stripping away the time-sensitive stack detail.

What remains valuable is the product and backend shape:

- multi-role logistics platform
- operational backend core
- realtime workflows
- pricing, routing, payment, and tracking support
- analytics and control-tower feedback loops

That is the part worth carrying forward.
