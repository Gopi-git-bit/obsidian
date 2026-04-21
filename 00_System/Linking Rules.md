# Linking Rules

Good linking turns the vault into a decision graph instead of a folder archive.

## Core Principles

### Rule 1: Every note should connect

- Avoid isolated notes.
- Prefer at least two meaningful related-note links.

### Rule 2: Atomic notes should link upward to a hub

Examples:

- `Fleet Utilization.md` -> [[Operations Strategy Hub]]
- `Load Matching Algorithm.md` -> [[Algorithms Hub]]

### Rule 3: Hubs should link downward to child notes

Inside `Algorithms Hub.md`:

```markdown
- [[Load Matching Algorithm]]
- [[Dynamic Pricing Logic]]
- [[Carrier Scoring Algorithm]]
```

### Rule 4: Scenario notes should link to execution notes

Every scenario should link to:

- at least one concept
- at least one algorithm
- at least one SOP

Example:

- `[[Closed Body Vehicle]]`
- `[[Route Risk Scoring]]`
- `[[SOP - Assign Secure Vehicle]]`

### Rule 5: Do not over-link

Only link:

- key concepts
- related mechanisms
- upstream hubs
- downstream applications

### Rule 6: Source notes should stay readable

Source notes should not try to link every concept inline. Prefer a small `Derived Notes` section such as:

```markdown
## Derived Notes
- [[Fleet Utilization]]
- [[Transportation Agent]]
- [[Truck Aggregator Model]]
```

### Rule 7: Use bidirectional links when retrieval matters

If two notes are often used together, link both ways.

Examples:

- [[Driver Assignment Logic]] <-> [[Fleet Utilization]]
- [[MSME Shipper Pain Points]] <-> [[Indian MSME Logistics Model]]

### Rule 8: Use consistent naming

- Hubs: `Operations Strategy Hub`
- Scenarios: `Scenario - No Own Fleet Available`
- SOPs: `SOP - Handle POD Disputes`
- Algorithms: `Carrier Scoring Algorithm`
- Concepts: `Proof of Delivery`

## Linking Syntax

- Basic link: use double brackets around an existing note title.
- Custom display text: use a pipe after the note title to set display text.

## If A Link Is Unresolved

1. Create the note if it is genuinely needed.
2. Otherwise replace it with the closest existing note.
3. Do not leave placeholder links in system notes.

## Example Decision Chain

```text
Scenario - Need 20 ft Truck Chennai to Trichy
  -> [[Driver Assignment Logic]]
    -> [[LCV vs MCV vs HCV]]
      -> [[Fleet Utilization]]
        -> [[Truck Aggregator Model]]
          -> [[Operations Strategy Hub]]
```

## Hub-To-Hub Linking

Valid examples:

- [[Operations Strategy Hub]] <-> [[Business Models Hub]]
- [[Algorithms Hub]] <-> [[Fleet & Transport Hub]]
- [[Customer Problems Hub]] <-> [[Market Intelligence Hub]]

## Review Habit

During each review cycle:

1. Check unresolved links in system notes first.
2. Find orphan notes.
3. Verify scenario notes still connect to concepts, algorithms, and SOPs.
4. Add or remove links intentionally rather than passively accumulating placeholders.

---

*Links are what make the vault navigable. Keep them honest.*
