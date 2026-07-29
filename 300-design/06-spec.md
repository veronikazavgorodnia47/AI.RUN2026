# SPEC.md — Availability Assistant

## AI-AC Refinements

### AI-AC1 (confidence) — AvailabilityBadge
- Component:   AvailabilityBadge
- Variant:     likely-available (confidence ≥ 0.7) / limited-availability (confidence < 0.7)
- Color token: color.amber-500 (likely) / color.amber-700 (limited)
- Typography:  typography.text-caption
- Placement:   below product price, above add-to-cart button
- Visual gate: IF confidence_score >= 0.7 THEN show likely-available variant
               ELSE show limited-availability variant
               No green state at any confidence level.

### AI-AC2 (fallback) — StoreCheckMessage
- Component:   StoreCheckMessage
- Variant:     fallback (replaces AvailabilityBadge)
- Color token: color.neutral-600
- Typography:  typography.text-body-regular
- Placement:   same position as AvailabilityBadge (below price, above add-to-cart)
- Visual gate: IF sap_sync_age > 30_minutes OR confidence_data == null
               THEN show StoreCheckMessage
               ELSE show AvailabilityBadge

### AI-AC4 (disclosure) — AvailabilityDisclosure
- Component:   AvailabilityDisclosure
- Variant:     timestamp-visible (default) / tooltip-expanded (on tap)
- Color token: color.neutral-500
- Typography:  typography.text-tooltip
- Placement:   info icon inline, right of AvailabilityBadge
- Visual gate: ALWAYS show timestamp_label + info_icon inline
               ON tap(info_icon) THEN show disclosure_tooltip:
               "Estimated from store data — not a guarantee."

---

## Components

### AvailabilityBadge
States: likely-available | limited-availability | loading | skeleton
Tokens: color.amber-500 (likely) / color.amber-700 (limited) /
        color.neutral-200 (skeleton)
Typography: typography.text-caption
Linked AC: AI-AC1, AI-AC3

### StoreCheckMessage
States: fallback
Tokens: color.neutral-600
Typography: typography.text-body-regular
Content: "Check in store" + store phone number
Linked AC: AI-AC2

### AvailabilityDisclosure
States: timestamp-visible | tooltip-expanded
Tokens: color.neutral-500
Typography: typography.text-tooltip
Content (timestamp): "Updated [X] min ago"
Content (tooltip): "Estimated from store data — not a guarantee."
Linked AC: AI-AC4

---

## Negative AC (carried verbatim from 04-ai-ac.md)
The assistant MUST NOT show a green "In stock" badge at any confidence level,
display exact unit counts, or promise a guaranteed hold.

---

## Asset and data references
- Confidence score: server-side computed field (0.0–1.0)
- SAP sync age: timestamp from inventory sync API
- Store phone number: store metadata API
- Prototype reference: `05-mockup.html`
