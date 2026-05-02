---
type: memo
domain: frontend
scope: transport_company_mobile
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[Operations Strategy Hub]]"
  - "[[Business Models Hub]]"
tags:
  - frontend
  - transport-company
  - fleet
  - dual-role
  - source-of-truth
source_files:
  - "C:\\Users\\user\\Downloads\\frontend transport.txt"
---

# Transport Company Frontend for Current Project

## Purpose

This note reshapes the older transport-company PRD for the current Zippy project state.

Transport companies remain strategically important, but the current MVP should not overbuild a broad marketplace before the core workflow is proven.

The transport-company frontend should support two practical realities:

- a company can provide vehicles and drivers to Zippy
- a company can place orders when it lacks capacity

## Current Transport Company Mission

The app helps transport-company managers:

- manage fleet availability
- assign drivers or vehicles to received work
- accept or reject provider-side opportunities
- place customer-side orders when capacity is short
- monitor active company trips
- view service fees, invoices, and settlement status
- maintain partner reliability and relationship health

## Role Model

Use role-aware workflows, but avoid making the UI feel like two unrelated apps.

Modes:

| Mode | Meaning |
|---|---|
| Provider Mode | company offers capacity and receives work |
| Customer Mode | company places shipment requests |

Important rule:

```text
same company identity, separate role context for ledgers, orders, and permissions
```

This follows the finance rule that transport-company customer-role and provider-role records must not be mixed.

## Recommended Navigation

Primary navigation:

- Dashboard
- Orders
- Fleet
- Finance
- Profile

Later addition:

- Network

The older PRD's partner marketplace is valuable, but it should be phased after corridor workflow proof.

## Current App Structure

```text
Transport Company App
├── Auth
│   ├── Login
│   └── Company Verification
├── Dashboard
│   ├── Role Context
│   ├── Fleet Availability
│   ├── Active Trips
│   └── Work Opportunities
├── Orders
│   ├── Received Work
│   ├── Placed Orders
│   └── Order Details
├── Fleet
│   ├── Vehicles
│   ├── Drivers
│   ├── Availability
│   └── Compliance
├── Finance
│   ├── Provider Earnings
│   ├── Customer Payments
│   ├── Service Fees
│   └── Invoices / Settlements
└── Profile
    ├── Company Details
    ├── Service Areas
    ├── Documents
    └── Settings
```

## Dashboard

Purpose:

- show whether the company has work, capacity, and blockers

Show:

- active operating mode
- available vehicles
- active provider trips
- active placed orders
- pending assignments
- document or compliance blockers
- payment or service-fee blockers
- reliability score

Avoid:

- decorative charts before operational workflows work

## Provider Mode

Provider mode supports received work.

Show:

- new opportunities
- required vehicle type
- pickup/delivery lane
- cargo category
- expected earning or service fee visibility
- SLA / promised window
- required documents
- accept/reject action
- assign vehicle/driver action

Rules:

- acceptance is a provider signal, not final lifecycle truth
- backend confirms assignment and trip creation
- company can assign only verified vehicles/drivers

## Customer Mode

Customer mode supports placed shipment requests.

Reuse customer-app logic where possible:

- booking details
- quote review
- payment mode
- tracking
- POD and invoice visibility

Important:

- customer-mode payments and provider-mode earnings must remain separated
- app copy should clearly show whether the company is paying or earning on that order

## Fleet Screen

Purpose:

- maintain live usable supply

Show:

- vehicles
- drivers
- current status
- service area
- document verification
- insurance/permit expiry
- availability
- current trip if assigned
- performance score

Useful actions:

- mark vehicle available/unavailable
- update location or service area
- assign driver
- upload/renew documents
- view vehicle trip history

## Finance Screen

Purpose:

- prevent ledger confusion for dual-role companies

Sections:

- Provider Earnings
- Customer Payments
- Zippy Service Fees
- Invoices
- Settlements

Rules:

- provider-side work may show INR 700 service fee or current approved policy
- customer-side orders show payable invoices, not provider payout
- final finance truth comes from backend finance events

## Profile And Verification

Sections:

- company information
- GST/PAN
- service areas
- vehicle categories
- owner/admin contacts
- operational contacts
- billing contacts
- documents and licenses
- bank details where applicable
- notification settings

Verification status should be visible and actionable.

## MVP Scope

Build first:

- company login/verification
- fleet and driver records
- provider work queue
- accept/reject opportunity
- assign vehicle/driver
- active trip visibility
- finance status split by role

Delay:

- public partner marketplace
- broad collaboration history
- advanced demand heat maps
- rich network discovery

## Success Metrics

- active verified vehicles
- vehicle availability accuracy
- provider acceptance rate
- assignment time
- cancellation rate
- on-time pickup and delivery
- service-fee collection status
- provider retention
- fleet utilization

## Bottom Line

The current transport-company frontend should be treated as:

```text
a role-aware fleet, work, and finance surface
that lets transport companies provide capacity or place orders
without mixing operational or financial truth
```

