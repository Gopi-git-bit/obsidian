# Note Templates

This note contains the standard templates for creating notes in the Logistics Brain vault.

## Template Types

| Type | Use For | Frontmatter Type |
|------|---------|------------------|
| [[Note Templates#Concept Template|Concept Template]] | Single ideas, definitions | `concept` |
| [[Note Templates#Scenario Template|Scenario Template]] | Decision situations | `scenario` |
| [[Note Templates#SOP Template|SOP Template]] | Action sequences | `sop` |
| [[Note Templates#Algorithm Template|Algorithm Template]] | Decision logic | `algorithm` |
| [[Note Templates#Business Model Template|Business Model Template]] | Business models | `business_model` |

## Quick Reference

## Concept Template

```markdown
---
type: concept
domain: [operations|fleet|transport|warehousing|pricing|compliance|customer|technology]
decision_value: [low|medium|high]
status: [seedling|evergreen]
related_hubs:
  - [Hub Name]
---

# [Concept Name]

## Definition
## Why it matters
## Key variables
## Decision impact
## Risks
## Related Notes
```

## Scenario Template

```markdown
---
type: scenario
domain: [transport|operations|fleet]
urgency: [low|medium|high]
decision_value: [low|medium|high]
actors: [customer, transport_company, dispatcher, driver]
region: India
status: [draft|verified]
related_hubs:
  - [Hub Name]
source_notes:
  - [Source Note]
---

# Scenario - [Situation Description]

## Situation
## Variables
## Decision questions
## Recommended response
## Risks
## Related SOPs
## Related Concepts
## Related Algorithms
```

## SOP Template

```markdown
---
type: sop
domain: [booking|dispatch|tracking|delivery|payments|exception|customer|driver]
owner: [operations|admin|support]
decision_value: [low|medium|high]
status: [draft|verified]
related_hubs:
  - [Hub Name]
---

# SOP - [Action Name]

## Trigger
## Preconditions
## Steps
## Exceptions
## Escalation
## Related Scenarios
```

## Algorithm Template

```markdown
---
type: algorithm
domain: [matching|pricing|routing|allocation|risk|forecasting]
decision_value: [low|medium|high]
inputs: [input1, input2]
outputs: [output1]
status: [draft|verified]
related_hubs:
  - [Hub Name]
---

# [Algorithm Name]

## Purpose
## Inputs
## Logic
## Rules
## Edge Cases
## Related Notes
```

## Business Model Template

```markdown
---
type: business_model
domain: [strategy|operations|marketing]
decision_value: [low|medium|high]
status: [exploring|verified]
related_hubs:
  - [Hub Name]
---

# [Business Model Name]

## Overview
## Value Proposition
## Revenue Stream
## Cost Structure
## Key Partners
## Key Activities
## Key Resources
## Customer Segments
## Channels
## Related Models
```

## Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Hubs | `[Domain] Hub` | Operations Strategy Hub |
| Scenarios | `Scenario - [Situation]` | Scenario - No Own Fleet Available |
| SOPs | `SOP - [Action]` | SOP - Handle POD Disputes |
| Algorithms | `[Function] Algorithm` or equivalent logic name | Load Matching Algorithm |
| Concepts | `[Term]` or `[Term] [Type]` | Proof of Delivery |

## Frontmatter Requirements

All non-source notes should include:

- `type`
- `domain`
- `status`
- `related_hubs`

## Linking Requirements

Every note should:

1. Link to at least two related notes.
2. Link upward to a hub.
3. Use double brackets for internal links.
4. Avoid placeholder links that will stay unresolved.

---

*Use templates consistently so the vault stays useful to both humans and agents.*
