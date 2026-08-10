---
title: Distractor–Felboar Spell-Consume
slug: demon-felboar-spell-consume
season: 14
modes:
- solo
tribes:
- demon
tags:
- season 14
- consume
- spells
- battlecry
core:
- 110664
- 132901
- 130298
addons:
- 96786
- 130662
- 132899
- 97408
- 126173
- 126924
- 100949
cycle: []
composition_minions:
- {card_id: 132901, count: 1, golden_count: 0}
- {card_id: 110664, count: 1, golden_count: 0}
- {card_id: 130298, count: 1, golden_count: 0}
composition_spells:
- {card_id: 132903, count: 1}
board_examples:
- stage: mid
  turn: 10
  timestamp: 760
  note: Start of Turn 10 before purchases, with Distractor and two Felboars already converting the spell economy into three independent scaled bodies.
  units:
  - {card_id: 130662, slot: 1, attack: 206, health: 206}
  - {card_id: 132901, slot: 2, attack: 167, health: 174}
  - {card_id: 110664, slot: 3, attack: 313, health: 324}
  - {card_id: 110664, slot: 4, attack: 210, health: 226}
  - {card_id: 132917, slot: 5, attack: 11, health: 14}
  - {card_id: 130298, slot: 6, attack: 6, health: 6}
- stage: end
  turn: 12
  timestamp: 1034
  note: A stable Tavern board before end-of-turn effects, with Devilish Distractor feeding two Felboars—including a 4k/4k Golden copy.
  units:
  - {card_id: 130662, slot: 1, attack: 631, health: 631}
  - {card_id: 132901, slot: 2, attack: 1.3k, health: 1.3k}
  - {card_id: 110664, slot: 3, attack: 4k, health: 4k, golden: true, annotation: Divine Shield}
  - {card_id: 110664, slot: 4, attack: 2.3k, health: 2.4k}
  - {card_id: 80740, slot: 5, attack: 172, health: 171}
  - {card_id: 96786, slot: 6, attack: 53, health: 55}
  - {card_id: 130298, slot: 7, attack: 9, health: 9}
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/41/demons-shop-buff
  comp_id: '41'
- type: firestone
  url: https://www.firestoneapp.com/battlegrounds/comps
  comp_id: demons_fermenter
source:
  type: youtube
  url: https://www.youtube.com/watch?v=WYybK8pRz8Y
  author: XQN
video:
  id: WYybK8pRz8Y
  timestamp: 694
source_published_at: '2026-08-06'
verified_at: '2026-08-10'
---

## Game plan

Cast targeted spells on [[card:132901|Devilish Distractor]] to permanently enlarge minions in Bob's Tavern, then let [[card:110664|Felboar]] consume those inflated shop stats. [[card:130298|Balinda Stonehearth]] doubles targeted spells, so the same action accelerates Distractor and advances Felboar's spell counter twice. [[card:96786|Brann Bronzebeard]] stays only while Battlecry economy keeps that loop moving.

This is a resource engine first and a large-Demon board second: spells and Battlecries must keep arriving or Felboar stops growing.

## How to build it

- **Bridge:** take spell generation and efficient Battlecries while keeping enough tempo to level.
- **Commit:** Distractor, repeatable targeted spells, and Felboar are the real signal. A lone Felboar eating ordinary shops is only direction.
- **Scale:** target Distractor before the relevant Felboar consume resolves, and keep the two Felboars separate when that improves resistance to single-target scam.
- **Finish:** keep more than one meaningful body when possible so a single scam answer does not erase all your stats.

## Practical cautions

Do not hoard resources so long that the shop-consuming turns never happen. The source retains Brann and Balinda while they multiply real actions, but they are support pieces—not excuses to leave a tiny board. [[card:130662|Twisted Wrathguard]] can absorb secondary scaling, but it is not the engine.

The proof is visible at 17:14: Devilish Distractor is 1.3k/1.3k, Golden Felboar reaches 4k/4k, and the second Felboar reaches 2.3k/2.4k. If the spell and consume actions are not producing that kind of acceleration, stop protecting every support piece and buy tempo.

## Imp-lusionist shop-buff route

[Sevel's Demon shop-buff game](https://www.youtube.com/watch?v=HHpCusxZk_k&t=399s) demonstrates an alternative resource package for the same consume family. [[card:132899|Imp-lusionist]] generates two [[card:132903|Methodical Madness]] spells when its Deathrattle resolves; [[card:97408|Titus Rivendare]] makes that Deathrattle trigger again. Each Madness then lets a chosen Demon consume two random Tavern minions, so the package supplies concrete repeatable fuel instead of waiting for naturally offered Tavern spells.

[[card:126173|Air Revenant]] and refreshes grow Tavern targets through Easterly Winds. [[card:126924|Flaming Enforcer]] converts the highest-Health target at end of turn, while Methodical Madness moves two random shop bodies onto the chosen Demon immediately. [[card:100949|Soul Rewinder]] is source-shown tempo support for the Demon shell; it is not the shop-scaling engine.

Commit to this variant when Imp-lusionist plus Titus can generate several Madness casts and you already have a Demon worth feeding. Do not hold a tiny Imp-lusionist/Titus board for a future payoff while ignoring immediate stats—the spells matter only when the Tavern has been meaningfully inflated. The Turn 15 recruit board around [21:00](https://www.youtube.com/watch?v=HHpCusxZk_k&t=1260s) shows the mature result with multiple six-figure bodies before the final boss at **21:56**.
