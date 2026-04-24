---
type: business-model
domain: business_models
decision_value: high
status: future-fit
related_hubs:
  - Business Models Hub
  - Operations Strategy Hub
  - Market Intelligence Hub
tags:
  - business-model
  - embedded-finance
  - msme
  - credit
  - settlement
  - partner-model
---

# Embedded Finance Enablement Framework

## Purpose

Describe how Zippy can support MSME payment flexibility through partners without becoming the direct lender or balance-sheet risk holder.

## Core Principle

Zippy should enable credit with verified logistics data, not fund credit with its own working capital.

## Why This Matters

- MSMEs often expect 15 to 45 day payment flexibility.
- Carrier and driver liquidity still depends on faster settlement.
- A marketplace that cannot address cash-flow friction may lose otherwise valid freight demand.

## Zippy Role Boundary

| Function | Zippy Role | Partner Role |
|---------|------------|--------------|
| Shipment and payment data | Provide verified operational evidence | Consume for underwriting |
| Credit scoring inputs | Compute platform-side trust or risk signals | Decide final approval model |
| KYC and lending compliance | Share only required verified metadata | Own regulated KYC and credit compliance |
| Disbursement and repayment | Receive approved settlement and track finance-linked order state | Fund, collect, and absorb default risk |
| Default exposure | Support collections workflow with evidence only | Own direct credit loss |

## Best-Fit Model

- Pay-later or invoice-finance options should appear as partner-led checkout choices.
- Lenders or NBFCs pay the platform or carrier according to approved terms.
- MSMEs repay the financing partner under agreed credit windows.
- Zippy monetizes conversion lift, referral economics, or settlement-speed advantage rather than interest spread.

## Useful Platform Signals

| Signal | Why It Helps |
|-------|--------------|
| Order frequency | Indicates business continuity and repeat demand |
| Payment timeliness | Helps separate reliable and stressed customers |
| POD and delivery completion quality | Confirms shipment truth and invoice confidence |
| Repeat-lane behavior | Improves predictability of receivables and operational trust |
| Dispute rate | Helps lenders understand operational friction and fraud risk |

## Operating Safeguards

1. Do not market internal credit capability before lender integration is real.
2. Keep underwriting, KYC, and default handling outside the core logistics agents.
3. Store finance-eligibility metadata separately from direct settlement truth.
4. Make all finance-partner actions auditable and event-linked.
5. Start with narrow customer cohorts and corridor-based pilots.

## Database and Workflow Direction

- Existing `payments`, `settlements`, and `invoices` structures remain the financial core.
- A future extension can add partner-finance request records, customer risk bands, and lender decision metadata without mixing them into the order-state machine.
- Credit-related workflow should be additive to settlement logic, not a replacement for it.

## Strategic Benefits

| Benefit | Reading |
|--------|---------|
| Higher conversion | Customers can book even when cash flow is temporarily tight |
| Faster carrier settlement | Supply-side trust improves without operator-funded float |
| Data moat | Shipment truth becomes commercially useful beyond routing and matching |
| Revenue upside | Referral, partner, or workflow monetization may emerge over time |

## Main Risks

| Risk | Why It Matters |
|------|----------------|
| Compliance overreach | The platform must not drift into unlicensed lending behavior |
| Poor risk signals | Weak data quality can damage lender trust and partner economics |
| Customer confusion | Payment flexibility must be explained as lender-led, not platform-funded |
| Integration complexity | Finance workflows can slow checkout if not tightly scoped |

## Recommended Starting Pattern

1. Build internal trust or risk segmentation from payment and delivery history.
2. Pilot partner-led pay-later for a narrow MSME segment.
3. Keep exposure off the Zippy balance sheet.
4. Expand only after repayment, dispute, and conversion metrics are stable.

## Related Notes

- [[Revenue Model Decision Framework]]
- [[Indian Road Logistics Pain Point Map]]
- [[Payment Settlement Agent]]
- [[Authoritative Database Schema]]
- [[Customer Terms & Privacy Policy Framework]]

## Related Hubs

- [[Business Models Hub]]
- [[Operations Strategy Hub]]
- [[Market Intelligence Hub]]
