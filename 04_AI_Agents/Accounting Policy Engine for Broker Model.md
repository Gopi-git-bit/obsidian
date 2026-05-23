---
title: Accounting Policy Engine for Broker Model
type: agent-architecture
category: accounting-policy
status: active
region: India
created: 2026-05-20
tags:
  - accounting
  - ind-as-115
  - broker-model
  - agent-model
  - revenue-recognition
  - gst
  - zippy-logistics
related:
  - Payment Invoice and Accounting Agent Architecture for Logistics Platform
  - Finance and Invoice Event Layer for Logistics Platform
  - GST for Logistics
  - Customer Terms & Privacy Policy Framework
---

# Accounting Policy Engine for Broker Model

## Purpose

This note defines Zippy's default accounting policy for standard marketplace transport transactions.

The policy is:

```text
Zippy operates as an agent/broker that arranges transport services between customers and independent drivers, vehicle owners, or transport vendors.
Zippy does not provide the physical transport service itself for standard marketplace transactions.
Zippy's revenue is limited to commission, platform fee, or brokerage/service fee.
Gross freight collected from the customer includes amounts payable to the vehicle owner/driver and should not be treated as Zippy's gross revenue.
```

## Ind AS 115 Alignment

Ind AS 115 principal-agent guidance supports this treatment when the entity's performance obligation is to arrange for another party to provide the specified service.

For Zippy:

| Fact | Accounting conclusion |
| --- | --- |
| Zippy arranges vehicles/drivers | Agent indicator |
| Zippy does not own the truck for standard marketplace transactions | Agent indicator |
| Driver/vehicle owner is responsible for carriage and delivery | Strong agent indicator |
| Zippy earns commission/platform fee | Net revenue model |
| Customer contracts with Zippy | Principal-risk indicator, requires contract wording control |
| Zippy fixes customer price | Principal-risk indicator, requires documentation and review flag |

Default classification:

```text
principal_agent_status = AGENT
revenue_presentation = NET_COMMISSION
```

## AccountingPolicyEngine Modules

```text
AccountingPolicyEngine
  ├── principal_agent_classifier          -> default: AGENT
  ├── revenue_recognition_rulebook        -> recognize commission after POD + OTP
  ├── gst_net_revenue_validator           -> GST not included in revenue
  ├── contract_liability_engine           -> customer advance held as liability
  ├── vendor_payable_accrual_engine       -> driver/owner payable after service completion
  ├── cut_off_testing_engine              -> month-end POD/OTP cut-off review
  ├── provision_and_claims_engine         -> claims allocated to responsible party
  ├── ecl_receivables_engine              -> credit risk on Zippy receivable only
  ├── suspense_close_blocker              -> no close/GST filing with material suspense
  └── audit_policy_version_registry       -> every policy version logged
```

## 1. Principal-Agent Classifier

Default policy:

```text
Zippy is classified as AGENT/BROKER for standard transport marketplace transactions.
```

Decision logic:

```text
IF
  zippy_legal_role = broker
  AND zippy_does_not_own_vehicle = true
  AND driver_or_vehicle_owner_responsible_for_delivery = true
  AND zippy_obligation = arrange_vehicle
  AND zippy_revenue_model = commission_only
THEN
  principal_agent_status = AGENT
  revenue_presentation = NET_COMMISSION
ELSE
  escalate_to_accounting_review
```

Risk flag:

```text
Customer-facing contract and pricing discretion exist.
Contract must clearly state that Zippy acts as broker/arranger and that transport responsibility remains with the vehicle owner, driver, or transport vendor.
```

Hard escalation:

```text
IF customer_contract_says_zippy_guarantees_delivery_or_compensation
OR zippy_assumes_primary_transport_responsibility
OR zippy_owns_or_controls_vehicle_for_this_transaction
THEN
  escalate_principal_agent_classification_review
```

## 2. Revenue Recognition Rulebook

Zippy's performance obligation:

```text
Arrange a suitable vehicle/driver for the customer and coordinate the shipment until verified POD + OTP confirmation.
```

Revenue trigger:

```text
Recognize commission revenue only after:
1. vehicle assigned
2. trip completed
3. POD uploaded and verified
4. OTP verified
5. no unresolved cancellation, fraud, dispute, or claim hold
```

Revenue rule:

```text
revenue_amount = commission_amount + platform_fee_amount
revenue_excludes = gross_freight_payable_to_driver_or_vehicle_owner
revenue_excludes_gst = true
```

## 3. Gross Freight Pass-Through Liability

On customer payment receipt:

```text
Dr Bank / Payment Gateway Control
    Cr Customer Advance / Freight Collection Liability
```

Do not post:

```text
Cr Freight Revenue
```

unless the transaction has been approved as principal/GTA or another principal transport model.

The liability contains:

```text
driver_payable_portion
zippy_commission_portion_not_yet_earned
gst_on_commission_not_yet_posted
```

## 4. Journal Entry Examples

Assumption:

```text
customer paid = INR 50,000
driver payable = INR 45,000
zippy commission = INR 5,000
GST on commission at 18 percent = INR 900
```

Customer payment received:

```text
Dr Bank / Payment Gateway Control                         50,000
    Cr Customer Advance / Freight Collection Liability    50,000
```

After POD + OTP, recognize Zippy commission:

```text
Dr Customer Advance / Freight Collection Liability         5,900
    Cr Commission Revenue                                  5,000
    Cr Output GST Payable                                    900
```

After POD + OTP, create driver payable:

```text
Dr Customer Advance / Freight Collection Liability        45,000
    Cr Driver / Vehicle Owner Payable                     45,000
```

When driver is paid:

```text
Dr Driver / Vehicle Owner Payable                         45,000
    Cr Bank / Payment Gateway Settlement                  45,000
```

## 5. GST Net Revenue Validator

Rule:

```text
IF revenue_model = NET_COMMISSION
THEN taxable_value_for_zippy = commission_amount_or_platform_fee
NOT gross_freight_amount
```

Validator:

```text
IF revenue_account_amount > commission_amount + platform_fee_amount
THEN block_journal("Possible gross revenue error under broker model")
```

Output GST:

```text
Cr Output GST Payable = commission_amount_or_platform_fee x applicable GST rate
```

The GST engine should still classify the exact tax path from supplier role, payer, invoice ownership, customer profile, and effective-dated GST rule version.

## 6. Contract Liability Engine

Before POD + OTP, customer money is not Zippy revenue.

```text
IF customer_payment_received = true
AND (pod_verified = false OR otp_verified = false)
THEN classify_as = Customer Advance / Freight Collection Liability
```

After POD + OTP:

```text
driver portion -> Driver / Vehicle Owner Payable
commission portion -> Commission Revenue + Output GST Payable
```

## 7. Vendor Payable Accrual Engine

Driver/vehicle-owner payable arises only after verified service completion.

```text
IF pod_verified = true
AND otp_verified = true
AND driver_claim_clear = true
THEN create Driver / Vehicle Owner Payable
```

If there is damage, shortage, accident, detention, fraud, or dispute:

```text
IF dispute_open = true
THEN hold driver payable in Vendor Payable Under Dispute
AND block final settlement release
```

## 8. Provision And Claims Engine

If the claim is recoverable from the driver/vehicle owner:

```text
Dr Driver / Vehicle Owner Payable
    Cr Claim Recovery / Settlement Adjustment
```

If Zippy has separately promised compensation to the customer:

```text
Dr Claims Expense
    Cr Provision for Customer Claims
```

Hard rule:

```text
IF customer_contract_says_zippy_guarantees_delivery_or_compensation
THEN escalate principal-agent classification and provision review
```

## 9. Cut-Off Testing Engine

Month-end treatment:

| Status at period end | Accounting treatment |
| --- | --- |
| Payment received, no POD/OTP | Liability only |
| Trip started, no POD/OTP | Defer commission revenue |
| POD done, OTP pending | Hold revenue |
| POD + OTP done before period end | Recognize commission revenue |
| POD after period end | Recognize next period unless approved evidence supports earlier completion |

Rule:

```text
IF pod_verified_at <= period_end
AND otp_verified_at <= period_end
THEN recognize commission in current period
ELSE defer commission
```

## 10. ECL Receivables Engine

For broker model:

```text
ECL applies only to:
1. unpaid commission receivable
2. customer receivable legally due to Zippy
3. recoverables from drivers, vehicle owners, or vendors
```

Do not calculate ECL on the full freight amount unless the full receivable legally belongs to Zippy.

## 11. Suspense Close Blocker

Close blocker:

```text
IF suspense_entries_open = true
THEN block:
  - monthly close
  - GST filing
  - investor MIS
  - statutory audit export
```

Allowed exception:

```text
immaterial non-GST, non-revenue timing items only
```

Never allow open suspense for:

- commission revenue
- GST payable
- customer advance / freight collection liability
- POD verification
- OTP verification
- driver payable
- payment gateway mismatch

## 12. Required Policy Fields

Every accounting policy decision should store:

| Field | Purpose |
| --- | --- |
| policy_id | unique accounting policy reference |
| policy_version | effective policy version |
| principal_agent_status | AGENT or PRINCIPAL |
| revenue_presentation | NET_COMMISSION or GROSS_FREIGHT |
| contract_risk_flag | customer-facing contract/pricing discretion warning |
| pod_verified_at | revenue cut-off evidence |
| otp_verified_at | revenue cut-off evidence |
| commission_amount | Zippy revenue basis |
| driver_payable_amount | pass-through liability basis |
| gst_taxable_value | GST basis for Zippy supply |
| review_required | accounting review flag |
| approved_by | reviewer if overridden |

## CA / Auditor Policy Statement

```text
Zippy operates as a logistics brokerage/marketplace platform. Zippy's performance obligation is to arrange transport services by connecting customers with independent drivers, vehicle owners, or transport vendors. Zippy does not own or operate the transport vehicle for standard marketplace transactions and does not assume primary responsibility for physical transportation of goods. Drivers/vehicle owners are responsible for the carriage and delivery of goods.

Accordingly, for standard marketplace transactions, Zippy acts as an agent and recognizes revenue on a net basis, limited to commission/platform fee. Gross freight collected from customers is treated as a pass-through collection liability to the extent payable to drivers/vehicle owners. Commission revenue is recognized only upon completion of Zippy's arranging/co-ordination obligation, evidenced by verified Proof of Delivery (POD) and OTP confirmation, provided no unresolved dispute, cancellation, fraud, or claim hold exists.
```

## Contract Wording Requirement

Customer terms must clearly state:

```text
Zippy arranges transport services.
The independent driver, vehicle owner, or transport vendor is responsible for physical carriage, delivery performance, loss/damage responsibility, and transport compliance.
```

Without this wording, the accounting engine must raise:

```text
principal_agent_contract_risk_review
```

## Source Links

- [MCA Ind AS 115 - Revenue from Contracts with Customers](https://www.mca.gov.in/Ministry/pdf/IndAS115_2020_10112020.pdf)
- [[Payment Invoice and Accounting Agent Architecture for Logistics Platform]]
- [[Finance and Invoice Event Layer for Logistics Platform]]
- [[GST for Logistics]]
