---
type: source
domain: zippy_logistics
status: processed
related_hubs:
  - "[[Indian Logistics Ecosystem Hub]]"
  - "[[Operations Strategy Hub]]"
  - "[[AI Agents Hub]]"
tags:
  - source
  - zippy-logistics
  - prd
  - specifications
actors:
  - Ai Logitech
region:
  - India
created: 2025-01-15
updated: 2025-01-15
source_file: claude.md
source_path: 02_Sources/claude.md
---

# Claude Source Document - Zippy Logistics Platform

## Overview

This is the primary source document containing all Product Requirements Documents (PRDs), specifications, and technical documentation for the Zippy Logistics platform. It was exported from Claude AI and contains comprehensive specifications for the Indian logistics operations system.

## Document Sections

### 1. Frontend Specifications

| App | Description | Key Features |
|-----|-------------|--------------|
| Driver Mobile App | Frontend specs for driver application | Order management, inventory, payments, notifications |
| Customer Mobile App | Frontend specs for customer application | Book shipment, track orders, payments |
| Transport Company App | Dual-role app for transport companies | Role toggle (Customer/Provider), fleet management |
| Admin Dashboard | Central command center for platform oversight | AI agent supervision, compliance, analytics |

### 2. Backend Architecture

- **7-Agent Architecture**: Customer Service, Order Management, Transportation, Resource Management, Payment & Settlement, Platform Administration, Communication
- **Agent Service Layer**: Python/Django implementation with agent communication
- **Database Schema**: PostgreSQL with refined tables for Indian logistics
- **Workflow Automation**: n8n-based workflow system

### 3. Technical Specifications

- **Commission Structure**: 10% from drivers, ₹700 flat fee from transport companies
- **Dual-Role System**: Transport companies can switch between Customer and Provider roles
- **AI Agent Framework**: Claude integration for logistics intelligence
- **Payment Processing**: Razorpay integration with GST compliance

---

## Derived Notes

This source document has been analyzed and expanded into the following atomic notes in the Logistics Brain:

### Hub Notes
- [[Indian Logistics Ecosystem Hub]] - India-specific logistics context
- [[AI Agents Hub]] - 7-agent architecture overview
- [[Fleet & Transport Hub]] - Fleet management concepts
- [[Business Models Hub]] - Commission and pricing models

### Algorithm Notes
- [[Route Optimization Logic]] - Route calculation algorithms
- [[Fleet Allocation Algorithm]] - Vehicle assignment logic
- [[Carrier Selection Algorithm]] - Partner selection criteria
- [[Payment Risk Logic]] - Financial risk assessment

### Scenario Notes
- [[Scenario - Vehicle Breakdown Mid-Route]] - Breakdown handling
- [[Scenario - Route Blocked Due to Protests]] - Route deviation scenarios
- [[Scenario - Driver Unavailable]] - Driver assignment issues
- [[Scenario - Partner Transporter Failure]] - Partner coordination

### SOP Notes
- [[SOP - Handle Vehicle Breakdown]] - Standard breakdown procedure
- [[SOP - Handle Partner Transporter]] - Partner coordination SOP
- [[SOP - Handle Delayed Shipment]] - Delay management

### AI Agent Notes
- [[Transportation Agent]] - Route optimization agent
- [[Resource Management Agent]] - Fleet allocation agent
- [[Payment Settlement Agent]] - Financial operations agent
- [[Platform Administration Agent]] - System governance agent
- [[Communication Agent]] - Notification management agent

### Ecosystem Notes
- [[Indian Road Freight Fragmentation]] - Market structure
- [[Tamil Nadu Industrial Corridors]] - Regional logistics
- [[Indian MSME Logistics Model]] - MSME sector focus
- [[Digital Freight Marketplace]] - Platform business model
- [[GST for Logistics]] - Tax compliance

---

## Key Business Rules

1. **Commission Deduction**:
   - Drivers: 10% commission deducted from earnings
   - Transport Companies: ₹700 flat service fee

2. **Role Switching**:
   - Transport companies can toggle between Customer (placing orders) and Provider (receiving orders) roles

3. **Payment Modes**:
   - Full Payment: 100% upfront
   - Part Payment: Minimum 50% advance
   - ToPay: Consignee pays upon delivery

4. **Alert Thresholds**:
   - Long Halt: >30 minutes stationary triggers alert
   - ETA Deviation: >4 hours triggers escalation

---

## Related Source Documents

- [[claude_source_index]] - Index of all source documents

---

*Source: Original Claude.md exported document containing Zippy Logistics comprehensive specifications*
