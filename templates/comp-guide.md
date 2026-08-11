---
title: Human-readable comp title
slug: lowercase-hyphenated-slug
season: 14
modes: [solo]
tribes: [beast]
tags: [deathrattle, scaling]
# Legacy compatibility fields; visual presentation comes from packages.
core: []
addons: []
cycle: []
packages:
  # Optional fixed section. Delete it entirely when there is no meaningful pre-core commitment signal.
  - title: Commit
    purpose: Explain why this signal opens the line without yet proving the final payoff.
    badge: Commit signal
    optional: false
    cards: []
  # Required fixed section. Keep this exact title and include the minimum defining engine.
  - title: Core
    purpose: One sentence explaining how the mandatory engine pieces interact.
    badge: Required core
    optional: false
    cards: []
  # Everything below Core is completely dynamic and may repeat card IDs from Commit/Core or another package.
  - title: Composition-specific package
    purpose: Explain the shopping role this package serves in this particular composition.
    badge: Composition-specific label
    optional: true
    cards: []
related_routes:
  - title: Alternative route title
    slug: existing-related-guide-slug
    purpose: One sentence explaining which core signal should make the player switch.
    cards: [] # One to three recognition-signature cards.
composition_minions: []
composition_spells: []
board_examples: []
discovery_sources:
  - type: hsreplay
    url: https://hsreplay.net/battlegrounds/comps/COMP_ID/comp-slug
    comp_id: 'COMP_ID'
  - type: firestone
    url: https://www.firestoneapp.com/battlegrounds/comps
    comp_id: firestone_comp_id
source:
  type: youtube
  url: https://www.youtube.com/watch?v=VIDEO_ID
  author: Creator name
video:
  id: VIDEO_ID
  timestamp: 0
source_published_at: 'YYYY-MM-DD'
verified_at: 'YYYY-MM-DD'
---

## How it works

Explain the demonstrated engine in one compact paragraph.

## Pivot signal

- State the concrete minimum signal that makes the line viable.
- State what is insufficient by itself.

## Positioning and traps

- Include only meaningful, source-supported positioning.
- Name the most likely way the engine fails.

## Useful timestamps

- **0:00** — Include only genuinely useful moments.
