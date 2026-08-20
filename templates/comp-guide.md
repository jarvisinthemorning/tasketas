---
title: Human-readable comp title
slug: lowercase-hyphenated-slug
season: 14
patch: '36.2.2'
modes: [solo]
tribes: [beast]
tags: [deathrattle, scaling]
classification: meta # Meta requires a composition-specific HSReplay discovery source; otherwise use variant, underdog, or highroll
# Legacy compatibility fields; visual presentation comes from packages.
core: []
addons: []
cycle: []
packages:
  # Optional. Include Commit only when a concrete pre-Core signal genuinely opens the line.
  # When present, it must be first and immediately followed by Core.
  # - title: Commit
  #   purpose: Explain the concrete early signal without pretending it is the finished engine.
  #   badge: Commit signal
  #   optional: false
  #   cards: [CARD_ID]
  # Core is always required and is first when Commit is omitted.
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
board_examples: [] # Screenshot-only. Prefer Tavern/start-of-turn; a readable late-game combat frame captured mid-fight is the fallback when no clean late frame exists.
# Example:
# - stage: early
#   turn: 7
#   timestamp: 320
#   phase: tavern
#   image: /static/boards/lowercase-guide-stage.webp
#   note: Short player-facing reason this snapshot is useful.
discovery_sources:
  - type: hsreplay
    url: https://hsreplay.net/battlegrounds/comps/COMP_ID/comp-slug
    comp_id: 'COMP_ID'
  - type: firestone
    url: https://www.firestoneapp.com/battlegrounds/comps
    comp_id: firestone_comp_id
# Optional strategy evidence for one variation or supporting claim. Keep one canonical primary source below.
supporting_sources:
  - type: youtube
    url: https://www.youtube.com/watch?v=SUPPORTING_VIDEO_ID
    author: Supporting creator
    label: Package or variation demonstrated
    timestamp: 0
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
