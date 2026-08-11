---
title: Mechs Magnetics
slug: mechs-magnetics
season: 14
modes:
- solo
tribes:
- mech
tags:
- season 14
- magnetic
- scaling
- mid-game pivot
classification: meta
core:
- 98592
- 132676
- 132312
addons:
- 98588
- 101314
- 120025
- 98576
- 129109
- 130798
cycle: []
packages:
- title: Commit
  purpose: Stay on the line only with Spark Snapper plus repeatable Magnetic supply; Scrap Scraper is the cleanest signal.
  badge: Snapper + supply
  optional: false
  cards: [132676, 98592]
- title: Core
  purpose: Generate improving Magnetizations, then double the best one onto Drone Duplicator.
  badge: Current Meta core
  optional: false
  cards: [132676, 98592, 132312]
- title: Magnetic supply
  purpose: Feed Snapper and create valuable Magnetizations; Titus can double Scrap Scraper's Deathrattle.
  badge: Keep resources flowing
  optional: true
  cards: [98592, 97408, 120025, 112364, 98582, 96812]
- title: Best duplication targets
  purpose: Activate Drone first, then attach your largest or most valuable Magnetic; Accord-o-Tron adds future Gold.
  badge: One deliberate Magnetization
  optional: true
  cards: [132312, 98576, 129109, 120025]
- title: End-turn payoff
  purpose: Utility Drone pays for every Magnetization already attached; Drakkari doubles that end-turn scaling.
  badge: Convert stacks into stats
  optional: true
  cards: [98588, 101314]
- title: Final carries
  purpose: Put stats behind protection or combat value instead of making one naked pile of numbers.
  badge: Survive scam and combat
  optional: true
  cards: [130798, 61930, 96812, 112364]
- title: Source high roll
  purpose: Wax Lance supplied a Tier 7 Sea Witch in Sevel's lobby; this raised the ceiling but did not define the comp.
  badge: Trinket-only ceiling
  optional: true
  cards: [133381, 103069]
composition_minions:
- {card_id: 132676, count: 1, golden_count: 0}
- {card_id: 98592, count: 1, golden_count: 0}
- {card_id: 132312, count: 1, golden_count: 0}
composition_spells: []
board_examples:
- stage: early
  turn: 9
  timestamp: 470
  phase: tavern
  image: /static/boards/mechs-magnetics-early.webp
  note: The transition still carries bridge bodies beside the developing engine; use this snapshot to judge what can remain while the comp comes online.
- stage: mid
  turn: 12
  timestamp: 785
  phase: tavern
  image: /static/boards/mechs-magnetics-mid.webp
  note: The engine now occupies most of the board while one flexible slot remains for utility or the next upgrade.
- stage: late
  turn: 13
  timestamp: 889
  phase: start_of_turn
  image: /static/boards/mechs-magnetics-late.webp
  note: A stable start-of-turn view of the mature board, useful for comparing permanent engine slots with the remaining replaceable support.
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/2/mechs-magnetics
  comp_id: '2'
source:
  type: youtube
  url: https://www.youtube.com/watch?v=ODSiIR9LlNI
  author: Sevel
video:
  id: ODSiIR9LlNI
  timestamp: 470
source_published_at: '2026-08-07'
verified_at: '2026-08-11'
---

## How it works

[[card:132676|Spark Snapper]] turns every Mech you play into another improving Magnetization. [[card:98592|Scrap Scraper]] supplies random Magnetic Mechs through its Deathrattle; [[card:97408|Titus Rivendare]] can multiply that supply when your hand has room for the generated cards and your board can field the Deathrattle package.

The current Meta shell adds [[card:132312|Drone Duplicator]]. Activate it **before** your chosen Magnetization, then attach the largest or most useful Magnetic you can afford that turn. [[card:98576|Accord-o-Tron]] is especially valuable because doubling its Magnetization also builds future Gold. Once several minions carry multiple Magnetizations, [[card:98588|Utility Drone]] converts that history into end-of-turn board scaling, and [[card:101314|Drakkari Enchanter]] doubles the payoff.

Sevel's game demonstrates the broader Magnetics engine, a Turn 9 pivot, Scrap Scraper supply, Spark Snapper scaling, Utility Drone payoff, protected late-game bodies, and a visible first-place finish. The current HSReplay Core also includes Drone Duplicator; the video does **not** visibly teach that card, so its role here follows its current card text rather than being attributed to Sevel.

HSReplay also lists [[card:133075|Captain Cookie]] and [[card:126916|Seafloor Recruiter]] as optional add-ons. Sevel does not teach that Chef's Choice branch, so it stays outside the primary shopping strip rather than being presented as source-backed sequencing.

## Pivot signal

- **Commit:** [[card:132676|Spark Snapper]] plus repeatable Magnetic supply, preferably [[card:98592|Scrap Scraper]]. A lone Snapper or one incidental Magnetic is not enough.
- **Core:** add [[card:132312|Drone Duplicator]] when offered, but do not freeze a functioning Snapper/Scraper transition while waiting for the perfect three-card board.
- **Mid-game friendly:** Sevel carries an unrelated early board and moves into Mechs around Turn 9. The line does not require banking Magnetics from the opening turns.
- **Current timing:** Spark Snapper is now Tavern Tier 5 after the 36.2.1 hotfix, so the commitment naturally happens later than a Tier 4 engine.

## Shopping and sequencing

1. Keep hand space for Scrap Scraper's generated Magnetic cards; reserve board slots separately for the engine and payoff pieces you still need to field.
2. Play ordinary Mechs while Spark Snapper is present to improve its Satellite Magnetizations.
3. Before attaching your best Magnetic, activate Drone Duplicator and confirm it is the intended target.
4. Prefer a large Magnetic or one with repeatable value—Gold from [[card:98576|Accord-o-Tron]], stat multiplication from [[card:129109|Timewarped Wargear]], or a valuable Deathrattle from [[card:120025|Auto Assembler]]—over merely copying a small keyword.
5. Add Utility Drone after you have real Magnetization density. Add Drakkari when it will double enough end-turn value to justify a board slot.
6. Finish with protected carries and combat utility rather than concentrating every stat on one vulnerable minion.

This is not an APM composition. The important actions are ordered, not frantic: make room, activate Drone, attach the chosen Magnetic, then resolve the rest of the turn.

## Positioning and traps

- [[card:98592|Scrap Scraper]] needs to die for its Deathrattle; do not hide it where combat cannot reach it when generation still matters.
- [[card:97408|Titus Rivendare]] multiplies Scrap Scraper's Deathrattle but does not create hand space. A full hand can waste the extra generation.
- [[card:132312|Drone Duplicator]] only doubles the next Magnetization **to itself** that turn. Activating it and then magnetizing another target wastes the setup.
- [[card:98588|Utility Drone]] rewards the number of Magnetizations already attached. Buying it before you have stacks is weak tempo.
- One enormous unprotected body can still lose to scam. Divine Shield, Reborn, multiple carries, and Deflect-o-Bot resets turn raw stats into a board that actually survives combat.
- Sevel's [[card:133381|Wax Lance]] produced [[card:103069|Sea Witch Zar'jira]]. That is a trinket-specific ceiling enhancer, not a reason to force the composition in an ordinary lobby.

## After a loss

- **Snapper's Satellites stayed small:** you committed without enough Mechs or Magnetic supply.
- **You generated cards but stayed small:** the line lacked Drone duplication, Utility Drone payoff, or enough time for the stacks to matter.
- **Scrap Scraper produced nothing useful:** check whether your hand was full or whether it survived combat.
- **Your largest unit disappeared:** you stacked one target without enough protection or distributed threat.
- **The turn felt too busy:** decide the Drone target before playing the turn; this engine rewards sequencing more than speed.
- **The source board looked unreachable:** subtract Wax Lance and Sea Witch from the comparison. Those were high-roll extras, not the baseline route.

## Useful timestamps

- **7:50** — Turn 9 Tavern board: the mixed early board has pivoted into Spark Snapper and Magnetics.
- **9:35** — Turn 10: Scrap Scrapers are visible in hand while Snapper, Auto Assembler, Utility Drone, and growing carries are online.
- **13:05** — Turn 12 mature Tavern board with several protected triple-digit Mechs.
- **14:49** — Clean late Tavern board before the final turn's effects.
- **16:10** — Final combat begins.
- **16:50** — The source visibly confirms first place.
