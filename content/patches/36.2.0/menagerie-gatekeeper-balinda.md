---
title: Menagerie — Gatekeeper + Balinda Tea Sets
slug: menagerie-gatekeeper-balinda
season: 14
patch: '36.2.0'
modes:
- solo
tribes:
- menagerie
tags:
- season 14
- tavern spells
- spell scaling
- menagerie
classification: variant
core:
- 133329
- 130298
addons:
- 119942
- 122674
- 132316
- 132921
- 120754
cycle: []
packages:
- title: Core
  purpose: Target Gatekeeper with scaled spells while Balinda repeats each cast, producing repeated Tea Set buffs.
  badge: Required core
  optional: false
  cards: [133329, 130298]
- title: Spell quality
  purpose: Keep the route only when Tavern spells are already scaling; Meditative is direct quality and Whelp can build Health through repeated Rally triggers.
  badge: Required — choose a quality engine
  optional: false
  cards: [119942, 122674]
- title: Targeted casts
  purpose: Buy cheap friendly-targeted spells; Conjurer and Castaway add repeatable or discoverable casts when the turn can afford them.
  badge: Shopping engine
  optional: false
  cards: [132316, 132921]
- title: Extra Tea Sets
  purpose: Par-tea Guest supplies another Tea Set while filling a missing minion type.
  badge: Optional — extra scaling
  optional: true
  cards: [120754]
related_routes:
- title: Dragons — Chromadrake Battlecries
  slug: dragons-chromadrake-battlecries
  purpose: Pivot to Dragons when Chromadrake generation, Brann and Kalecgos are established before Gatekeeper plus Balinda appears.
  cards: [132955, 96786, 60630]
composition_minions:
- {card_id: 133329, count: 1, golden_count: 0}
- {card_id: 130298, count: 1, golden_count: 0}
- {card_id: 119942, count: 1, golden_count: 0}
composition_spells: []
board_examples:
- stage: mid
  timestamp: 719
  phase: tavern
  image: /static/boards/menagerie-gatekeeper-balinda-mid.webp
  note: A stable Recruit turn after the engine is assembled, showing the board-space pressure before another scaling cycle.
discovery_sources:
- type: firestone
  url: https://www.firestoneapp.com/battlegrounds/comps
  comp_id: neutral_tea_set
supporting_sources:
- type: youtube
  url: https://www.youtube.com/watch?v=7XRXuOyOfHQ
  author: Shadybunny
  label: Golden and all-type ceiling; not the minimum route
  timestamp: 793
- type: youtube
  url: https://www.youtube.com/watch?v=Ic08mTl1-HA
  author: JeefHS
  label: Player-perspective Gatekeeper and Balinda execution
  timestamp: 465
source:
  type: youtube
  url: https://www.youtube.com/watch?v=C1wCL3B6hA0
  author: Shadybunny
video:
  id: C1wCL3B6hA0
  timestamp: 618
source_published_at: '2026-08-08'
verified_at: '2026-08-13'
---

## How it works

[[card:133329|Gatekeeper Amalgam]] casts a [[card:105271|Misplaced Tea Set]] whenever you target it with a spell. [[card:130298|Balinda Stonehearth]] repeats the targeted cast, so one spell triggers Gatekeeper more than once. Spell-quality gains apply to every resulting Tea Set, turning cheap targeted spells into broad permanent Menagerie scaling.

## When to commit

- **Require the interaction, not one shiny six-drop.** Gatekeeper plus Balinda is the Core, but it is not enough without improved Tavern spells and casts you can afford.
- **Carry spell quality into the pivot.** [[card:119942|Tranquil Meditative]] is the cleanest direct engine. Repeated [[card:122674|Blue Whelp]] Rally triggers can provide the Health side shown by the source.
- **Keep type coverage.** Tea Set buffs one friendly minion of each type. A board full of duplicated types wastes casts.
- **Abort when casts are weak or scarce.** Gatekeeper without spell quality is slow; Balinda without useful targets is a six-Gold ornament.

## How to play it

1. **Build spell quality before forcing Gatekeeper.** The source explicitly identifies spell power as mandatory. Preserve a stable board while improving Tavern spells.
2. **Assemble Gatekeeper and Balinda.** Once both are live, direct friendly-targeted spells into Gatekeeper to multiply Tea Set triggers.
3. **Shop for casts, not decorative bodies.** Cheap targeted spells are the fuel. [[card:132316|Cagey Conjurer]] can repeatedly cast a spell on itself when that random cast is useful; [[card:132921|Clever Castaway]] discovers another Tavern spell.
4. **Maintain type diversity and one working slot.** Cycle temporary spell suppliers and weak duplicate types. If the board and hand are locked, the engine cannot convert resources efficiently.
5. **Treat golden and all-type pieces as ceiling.** The supporting game adds premium golden pieces, all-type conversions and exceptional economy. They increase cast count and coverage but are not the honest entry condition.

## Positioning and traps

Combat order is not the defining decision; Recruit-phase spell targeting and board space are. Protect the strongest combat bodies for the opponent you face, but do not preserve a weak minion merely because it supplies a duplicate type.

Common losses come from committing before spell quality exists, spending too much Gold discovering casts, or keeping so many engines that the scaled Menagerie has no room for final utility.

## Why this is a Variant

Firestone currently tracks the route as **Neutral Tea Set**, so it is not an untracked Underdog. It is also mechanically different from the related Dragon guide: Chromadrakes may help improve or supply spells, but this composition wins by repeatedly converting targeted casts through Gatekeeper and Balinda rather than by scaling Dragons with Kalecgos.

## Useful timestamps

- **4:17** — the source explains the Chromadrake and Whelp spell-quality setup.
- **9:47** — Gatekeeper becomes the proposed payoff for the accumulated spell quality.
- **10:18** — Gatekeeper, Tea Set and Balinda's repeated-cast interaction is explained directly.
- **11:59** — the route is assembled while the source discusses which spell-quality support to retain.
- **14:09** — a targeted cast demonstrates the chain reaction.
- **17:45** — the source states the key failure condition: without spell quality, the composition does not work.
