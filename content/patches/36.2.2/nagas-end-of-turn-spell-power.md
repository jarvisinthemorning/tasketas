---
title: Nagas — End-of-Turn Spell Power
slug: nagas-end-of-turn-spell-power
season: 14
patch: 36.2.2
modes: [solo]
tribes: [naga]
tags: [end-of-turn, spell-power, scaling, menagerie]
classification: meta
core: [120299, 120905, 101314, 130298, 133329]
addons: [120905, 101314, 130298, 133329]
cycle: []
packages:
  - title: Commit
    purpose: Felfire plus Drakkari gives you a real spell-power direction; plan to reach Tier 6 for the payoff.
    badge: Commit signal
    optional: false
    cards: [120299, 101314]
  - title: Core
    purpose: Build spell power, repeat Fauna's targeted casts, and convert them into permanent board-wide stats.
    badge: Required core
    optional: false
    cards: [120299, 120905, 101314, 130298, 133329]
  - title: Multipliers
    purpose: Extra copies compound the same end-of-turn cast instead of adding a separate engine.
    badge: Optional — scaling upgrades
    optional: true
    cards: [120905, 101314, 130298]
  - title: Permanent targets
    purpose: Keep Gatekeeper beside Fauna so every repeated targeted spell becomes permanent team scaling.
    badge: Optional — final carries
    optional: true
    cards: [133329]
related_routes: []
composition_minions:
  - card_id: 120299
    count: 1
    golden_count: 0
  - card_id: 120905
    count: 1
    golden_count: 0
  - card_id: 101314
    count: 1
    golden_count: 0
  - card_id: 130298
    count: 1
    golden_count: 0
  - card_id: 133329
    count: 1
    golden_count: 0
composition_spells: []
board_examples:
  - stage: late
    timestamp: 1100
    phase: tavern
    image: /static/boards/nagas-end-of-turn-spell-power-late.webp
    note: A stable late Tavern turn showing the completed engine before its next end-of-turn trigger.
discovery_sources:
  - type: hsreplay
    url: https://hsreplay.net/battlegrounds/comps/55/nagas-end-of-turn-spell-buff
    comp_id: '55'
supporting_sources: []
source:
  type: youtube
  url: https://www.youtube.com/watch?v=itEcEPfqfbE
  author: Shadybunny
video:
  id: itEcEPfqfbE
  timestamp: 407
source_published_at: '2026-08-20'
verified_at: '2026-08-20'
---

## How it works

[[card:120299|Felfire Conjurer]] improves the Tavern spells that give stats, then [[card:120905|Fauna Whisperer]] casts its targeted spell on adjacent minions at the end of the turn. [[card:101314|Drakkari Enchanter]] repeats that end-of-turn trigger, while [[card:130298|Balinda Stonehearth]] makes each targeted cast happen again. Put [[card:133329|Gatekeeper Amalgam]] beside Fauna: every cast on it triggers another team-wide permanent buff. The result is a compact chain—spell-power quality → repeated targeted casts → permanent scaling across the board.

## When to commit

- **Real signal:** [[card:120299|Felfire Conjurer]] plus [[card:101314|Drakkari Enchanter]], enough health to reach Tier 6, and a plausible path to Fauna or Balinda.
- **Do not force from one card:** Felfire alone improves future spells but does not create the repeated end-of-turn engine.
- [[card:120905|Fauna Whisperer]] is the mechanical handoff. Once Fauna joins Felfire and Drakkari, stop shopping as though you are still directionless.
- [[card:133329|Gatekeeper Amalgam]] is the preferred permanent recipient; without a strong target, your repeated casts produce much less lasting board value.

## Transition and shopping

1. Stabilize first. The source reaches its direction from a weak board only because it preserves health and buys time; do not copy the greed when you are already dying.
2. Use Felfire and Drakkari as the bridge, then prioritize Fauna. The first functional engine matters more than speculative triples.
3. Add Balinda once targeted casts are online. It multiplies the spells Fauna creates rather than merely adding a small fixed buff.
4. Place Gatekeeper beside Fauna and keep the second adjacent slot on another body you are happy to scale.
5. After the five-piece engine works, extra Fauna, Drakkari, and Balinda copies are your best scaling upgrades. Goldens are the ceiling, not the entry requirement.

## Positioning and sequencing

- End-of-turn order matters. Put [[card:120299|Felfire Conjurer]] before [[card:120905|Fauna Whisperer]] so the spell-power improvement happens before Fauna casts.
- Fauna must be adjacent to the minions you want to receive its spell. Keep [[card:133329|Gatekeeper Amalgam]] next to it.
- [[card:101314|Drakkari Enchanter]] and [[card:130298|Balinda Stonehearth]] do not need to be adjacent to Fauna; protect the adjacency slots for permanent targets.
- Late in the game, only cut a multiplier when another combat body solves a problem that additional scaling cannot—for example, immediate scam protection against the final opponent.

## What the source highrolled

The demonstrated game gets substantial acceleration from Elise producing premium Golden pieces and Faceless copying one of them. Shadybunny explicitly calls it a major highroll. Those effects explain the spectacular ceiling, but they are **not** part of this guide's Core. The transferable route is the five-card end-of-turn chain above.

## Common failure modes

- **Committed from Felfire alone:** you improved spells but never assembled the repeatable cast engine.
- **Reached Tier 6 without enough health:** the comp has several expensive pieces and cannot repair a lost transition by magic. Tragically, the Tavern does not accept optimism as currency.
- **Wrong end-of-turn order:** Fauna casts before Felfire improves the spell.
- **Poor adjacency:** Fauna repeatedly buffs expendable support bodies instead of permanent targets.
- **Chased the video ceiling:** Golden multipliers accelerated by Elise are a highroll, not the baseline shopping plan.
- **Kept adding fixed scaling after spell power was online:** once Fauna, Balinda, and Drakkari are functioning, buy multiplicative upgrades and durable targets instead.

## Useful timestamps

- **6:47** — Drakkari plus Felfire establishes the direction.
- **9:43** — Fauna arrives and the end-of-turn engine comes together.
- **10:26** — The source discusses Fauna adjacency and end-of-turn ordering.
- **11:47** — Balinda becomes the next multiplier.
- **14:31** — Explanation of why repeated spell-power casts beat a small fixed scaling addition.
- **17:06** — Explicit warning that Elise and Faceless made this a major highroll.
- **18:20** — Stable late Tavern board with the completed engine.
