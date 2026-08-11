---
title: Dragons — Chromadrake Battlecries
slug: dragons-chromadrake-battlecries
season: 14
modes:
- solo
tribes:
- dragon
tags:
- season 14
- battlecry
- rally
- scaling
- chromadrakes
classification: underdog
core:
- 132955
- 132957
- 60630
- 96786
addons:
- 132951
- 126860
- 92413
- 133329
- 132953
cycle: []
packages:
- title: Commit
  purpose: Pair Bronze Timewalker with Sky-hatch Runaway; neither card alone establishes the Rally loop.
  badge: Commit signal — paired generator
  optional: false
  cards: [132955, 132957]
- title: Core
  purpose: Trigger Timewalker with Runaway, double the generated Chromadrake Battlecries with Brann, and turn every trigger into permanent Dragon stats with Kalecgos.
  badge: Required core
  optional: false
  cards: [132955, 132957, 60630, 96786]
- title: Mount generator
  purpose: Hired Mount is the simpler one-card alternative when its Activate cost fits the turn.
  badge: Optional — alternative generator
  optional: true
  cards: [132951]
- title: More Chromadrakes
  purpose: Add generated Battlecries without filling every permanent board slot with setup pieces.
  badge: Optional — supply upgrades
  optional: true
  cards: [126860, 132951]
- title: Final carries
  purpose: Convert the broad permanent scaling into protected attackers and efficient late bodies.
  badge: Optional — late upgrades
  optional: true
  cards: [92413, 133329, 132953]
- title: Source highrolls
  purpose: These accelerate Battlecries or golden pieces, but the Tavern-minion engine must already work without them.
  badge: Optional — source ceiling
  optional: true
  cards: [133403, 112082]
related_routes: []
composition_minions:
- {card_id: 132955, count: 1, golden_count: 0}
- {card_id: 132957, count: 1, golden_count: 0}
- {card_id: 60630, count: 1, golden_count: 0}
- {card_id: 96786, count: 1, golden_count: 0}
- {card_id: 92413, count: 1, golden_count: 0}
- {card_id: 133329, count: 1, golden_count: 0}
composition_spells: []
board_examples:
- stage: end
  turn: 14
  timestamp: 1240
  phase: tavern
  image: /static/boards/dragons-chromadrake-battlecries-end.webp
  note: The last stable Tavern turn before the verified first-place combat, useful as a mature-route benchmark.
supporting_sources:
- type: youtube
  url: https://www.youtube.com/watch?v=-bP5beZRYW4
  author: Shadybunny
  label: Bronze Timewalker plus Sky-hatch Runaway Rally generator
  timestamp: 533
- type: youtube
  url: https://www.youtube.com/watch?v=VDLCBxk_-48
  author: Shadybunny
  label: Warpwing and Crimson Vindicator highroll package
  timestamp: 945
source:
  type: youtube
  url: https://www.youtube.com/watch?v=dCwe93sXIiM
  author: Sevel
video:
  id: dCwe93sXIiM
  timestamp: 930
source_published_at: '2026-08-05'
verified_at: '2026-08-11'
---

## Game plan

Generate Chromadrakes by using [[card:132957|Sky-hatch Runaway]] to trigger [[card:132955|Bronze Timewalker]], play their Battlecries through [[card:96786|Brann Bronzebeard]], and let [[card:60630|Kalecgos, Arcane Aspect]] turn every trigger into permanent stats across the Dragon board. [[card:132951|Hired Mount]] is the simpler one-card generator when you can spare its Activate cost.

The current source wins with Hired Mount, two Kalecgos, Brann, repeatable Chromadrake generation, and a flexible late board; the supporting source demonstrates the Timewalker-plus-Runaway Rally generator with double Kalecgos. Both sources use premium accelerants, but those rewards are not included in Core: the defining loop uses ordinary Tavern minions.

## When to commit

- **Rally route:** commit when Bronze Timewalker is already paired with Sky-hatch Runaway. Timewalker alone does not trigger its own Rally, and Runaway without a useful Rally target is not a composition.
- **Mount route:** use Hired Mount as the lower-commitment alternative when your board is stable enough to pay its Activate cost repeatedly and you can still level toward Kalecgos and Brann.
- **Finish the Core:** Kalecgos is the permanent scaling payoff and Brann multiplies each generated Battlecry. Do not keep buying low-tempo setup while waiting indefinitely for both.
- **Abort:** if the generator is draining Gold without producing enough tempo, or Tier 5 offers a stronger established route before Kalecgos appears, pivot instead of treating a future Dragon as a debt the Tavern owes you.

## How to play it

1. **Open a real generator.** Assemble Timewalker plus Runaway, or activate Hired Mount when the Gold does not cost a combat. [[card:126860|Draconic Warden]] adds burst supply later without demanding another permanent setup slot.
2. **Preserve space.** Keep one board slot and enough hand room before generating Chromadrakes. The primary source visibly runs into a full-hand sequencing problem; making more cards than you can play is just elaborate confetti.
3. **Play Battlecries through Brann.** Generated Chromadrakes provide the repeated Battlecry volume. With Kalecgos present, every trigger also buffs the Dragon board permanently.
4. **Cycle, do not collect.** Use the generated Battlecry, then sell the weakest temporary body unless it has become one of your best scaled Dragons. A seven-piece museum display switches off the engine.
5. **Upgrade the payoff.** The cited games show additional Kalecgos copies and golden engine pieces raising the ceiling. [[card:92413|Warpwing]], [[card:133329|Gatekeeper Amalgam]], and [[card:132953|Crimson Vindicator]] are optional late bodies, not pieces the evidence supports forcing from behind.

## Positioning

The cited sources do not establish one mandatory attack order. Brann, Kalecgos, and the generators do their defining work during the Recruit phase; arrange the actual combat board for the opponent rather than copying the recorded screenshot slot for slot.

## Why this is Underdog

The current complete directory audit found no HSReplay or Firestone composition whose Core is the Dragon/Kalecgos Chromadrake loop. Firestone does list a different **Neutral Tea Set** route that can use Chromadrake generation, but its Core is Brann, Balinda Stonehearth, and Gatekeeper Amalgam—not this Dragon composition.

This route is therefore classified **Underdog**, not Meta. Its minimum loop uses ordinary Tavern cards: Hired Mount or Timewalker-plus-Runaway supplies Chromadrakes, Brann doubles their Battlecries, and Kalecgos converts those triggers into permanent Dragon stats. [[card:133403|Dragon's Eye]], [[card:112082|Goldenizer Supply]], Dark Gifts, hero powers, and multiple golden engine pieces accelerate that loop but are not required by its card mechanics.

Evidence confidence is lower than for a tracked Meta guide: both full-loop examples reach their demonstrated ceiling with premium acceleration. The Underdog label applies to the reproducible minimum engine, not as a claim that the source's four-digit final board is an ordinary result.

## Common failure modes

- **Forced from one card:** Timewalker without Runaway, or Mount without spare Gold, is value—not a finished composition.
- **No permanent payoff:** generating Chromadrakes without Kalecgos or another established scaling plan creates motion rather than strength.
- **Board or hand locked:** full spaces prevent you from playing and selling the generated Battlecries that make the route work.
- **Too much engine:** multiple generators can consume the Gold and slots needed for final carries.
- **Chasing the video:** premium trinkets and golden pieces improve the source game; waiting for the same rewards turns an ordinary line into a self-inflicted Highroll.

## Useful timestamps

- **5:44** — Sevel finds Brann and starts evaluating the Dragon line.
- **7:22** — the source takes an extra-Dragon-Battlecry accelerator; useful ceiling evidence, not part of Core.
- **11:43** — generated Chromadrake value becomes central to the turn.
- **15:38** — repeatable Activate generation produces two more Chromadrakes.
- **20:40** — last stable Tavern turn before the winning combat.
- **21:52** — first place is visibly confirmed.
- **Shadybunny 8:53** — the supporting source demonstrates Sky-hatch Runaway triggering the Dragon Rally package.
- **Shadybunny 10:10** — double Kalecgos and the accelerated Runaway line are established.
- **Shadybunny Eudora 15:45** — related Warpwing/Vindicator ceiling; Dark Gift and hero interactions make this highroll context only.
