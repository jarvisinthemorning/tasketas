---
title: Naga — Fauna End-of-Turn Spells
slug: naga-fauna-end-of-turn-spells
season: 14
modes: [solo]
tribes: [naga]
tags: [season 14, spells, end of turn, scaling]
classification: variant
core: [119942, 120905, 101314, 130298]
addons: [133707, 114816, 126916]
cycle: []
packages:
- title: Commit
  purpose: Pair Fauna with established Tavern-spell quality; either card alone is only setup.
  badge: Commit signal — quality plus caster
  optional: false
  cards: [119942, 120905]
- title: Core
  purpose: Fauna casts improved Natural Blessings at end of turn; Drakkari repeats the trigger and Balinda repeats each targeted cast.
  badge: Required core
  optional: false
  cards: [119942, 120905, 101314, 130298]
- title: Payoffs
  purpose: Ruiner converts every cast on a Naga into board-wide stats; Groundbreaker rewards the accumulated spell count and Naga cycling.
  badge: Optional — scaling payoffs
  optional: true
  cards: [133707, 114816]
- title: Naga targeting
  purpose: Recruiter can turn another body into a Naga so Fauna and Ruiner can scale useful non-Naga support.
  badge: Optional — type utility
  optional: true
  cards: [126916]
related_routes:
- title: Naga Balinda–Torrential Ruiner Spell Burst
  slug: naga-balinda-torrential-ruiner
  purpose: Pivot to the burst route when Balinda plus Ruiner and immediate targeted-spell density arrive before Fauna's end-of-turn engine.
  cards: [130298, 133707]
composition_minions:
- {card_id: 119942, count: 1, golden_count: 0}
- {card_id: 120905, count: 1, golden_count: 0}
- {card_id: 101314, count: 1, golden_count: 0}
- {card_id: 130298, count: 1, golden_count: 0}
composition_spells: []
board_examples:
- stage: mid
  turn: 11
  timestamp: 820
  phase: tavern
  image: /static/boards/naga-end-of-turn-spells-mid.webp
  note: A clean Recruit-phase view after the end-of-turn engine is established, with the complete board and shop visible.
discovery_sources:
- type: firestone
  url: https://www.firestoneapp.com/battlegrounds/comps
  comp_id: naga_end_of_turn
supporting_sources: []
source:
  type: youtube
  url: https://www.youtube.com/watch?v=Us-HN9FXZxc
  author: Rdu Hearthstone
video:
  id: Us-HN9FXZxc
  timestamp: 620
source_published_at: '2026-08-05'
verified_at: '2026-08-13'
---

## How it works

[[card:119942|Tranquil Meditative]] permanently improves Tavern spells. [[card:120905|Fauna Whisperer]] casts Natural Blessing on both neighbors at the end of the turn; [[card:101314|Drakkari Enchanter]] repeats that end-of-turn trigger, while [[card:130298|Balinda Stonehearth]] repeats each friendly-targeted cast. Unlike the related Ruiner burst route, this composition invests in a recurring end-of-turn engine.

## When to commit

- **Start from Fauna plus spell quality.** Fauna with unimproved blessings is too slow; Meditative without a repeatable caster does not define this route.
- **Finish the multiplier layer.** Drakkari increases Fauna triggers and Balinda increases each targeted cast. Finding either makes the pair viable; both provide the tracked route's full ceiling.
- **Do not force from Torrential alone.** [[card:133707|Torrential Ruiner]] is an excellent payoff, but the route remains Fauna-driven.
- **Abort if one slow turn kills you.** The scaling lands at end of turn. Spend for immediate tempo when the next opponent demands it.

## How to play

1. **Improve Tavern spells.** Use Meditative's Spellcraft repeatedly before expecting Fauna's Natural Blessings to carry combat.
2. **Place Fauna between the two bodies you want scaled.** Its casts target adjacent minions; empty or disposable neighbors waste the trigger.
3. **Add Drakkari and Balinda.** They multiply different parts of the engine, so their effects stack rather than replacing one another.
4. **Convert casts into broader value.** Ruiner rewards spells cast on a Naga with board-wide stats. [[card:126916|Seafloor Recruiter]] can make a chosen support body count as Naga when that improves your targeting.
5. **Trim economy late.** The source treats Brann as economy and looks to replace the final flex slot with combat utility once the engine is established.

## Positioning and traps

Fauna must sit between the intended recipients before the turn ends. Do not let a temporary economy body occupy an adjacent slot by accident; the game is quite capable of following your bad instructions perfectly.

The main failure modes are weak spell quality, missing a multiplier, or filling the board with engines and leaving no room for useful combat bodies. A second Fauna or Ruiner raises the ceiling, but neither repairs an unstable board by itself.

## Why this is a separate Variant

Firestone tracks **Naga End Of Turn** with Meditative, Fauna, Drakkari and Balinda as its Core. Our related Highroll guide instead commits through Balinda plus Torrential Ruiner and spends many targeted spells immediately. The routes share cards, but their timing, shopping priorities and minimum engines are different enough to deserve separate pages.

## Useful timestamps

- **7:29** — Rdu identifies Torrential Ruiner as a strong Naga payoff.
- **9:09** — targeted-spell placement becomes the central Recruit-phase decision.
- **10:13** — targeting Naga and developing Fauna are discussed.
- **11:21** — Balinda is identified as the major multiplier.
- **13:29** — the source emphasizes Balinda's value as the engine scales.
- **17:33** — Rdu calls the Naga build strong and starts refining the final board.
- **18:43** — a second Fauna is the remaining scaling upgrade he wants.
