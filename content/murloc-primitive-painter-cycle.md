---
title: Tidecaller–Tidehunter Handbuff APM
slug: murloc-primitive-painter-cycle
season: 14
modes:
- solo
tribes:
- murloc
tags:
- season 14
- handbuff
- spell targeting
- apm
core:
- 133026
- 132989
- 96786
addons:
- 132883
- 98509
- 98948
- 126637
cycle:
- 60028
- 133075
- 131145
board_examples:
- stage: mid
  timestamp: 1230
  note: "The spell-target handbuff engine is established: Tidecaller grows the hand, Tidehunter concentrates extra stats, and two Chorals convert that hand growth into a durable board."
  units:
  - {card_id: 133026, slot: 1, attack: 733, health: 480}
  - {card_id: 126637, slot: 2, attack: 458, health: 388}
  - {card_id: 98948, slot: 3, attack: 215, health: 230}
  - {card_id: 132989, slot: 4, attack: 979, health: 572}
  - {card_id: 98948, slot: 5, attack: 467, health: 395}
  - {card_id: 120677, slot: 6, attack: 852, health: 498}
- stage: late
  timestamp: 1390
  note: "A mature pre-combat Tavern board with Tidehunter over 1k and six permanent Murlocs; the following combat is won, but the source does not clearly show a first-place result screen."
  units:
  - {card_id: 133026, slot: 1, attack: 791, health: 504}
  - {card_id: 126637, slot: 2, attack: 516, health: 482}
  - {card_id: 98948, slot: 3, attack: 273, health: 324}
  - {card_id: 132989, slot: 4, attack: 1.1k, health: 674}
  - {card_id: 98948, slot: 5, attack: 525, health: 489}
  - {card_id: 120677, slot: 6, attack: 920, health: 599, annotation: Divine Shield}
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/67/murlocs-apm
  comp_id: '67'
composition_minions:
- {card_id: 133026, count: 1, golden_count: 0}
- {card_id: 132989, count: 1, golden_count: 0}
- {card_id: 98948, count: 1, golden_count: 0}
- {card_id: 126637, count: 1, golden_count: 0}
composition_hand_minions:
- {card_id: 98509, count: 1, golden_count: 0}
composition_spells: []
source:
  type: youtube
  url: https://www.youtube.com/watch?v=Ppj60f3j_AE
  author: Shadybunny
video:
  id: Ppj60f3j_AE
  timestamp: 388
source_published_at: '2026-08-02'
verified_at: '2026-08-08'
---

## Game plan

[[card:133026|Shamanic Tidecaller]] turns every Tavern Spell targeted at a Murloc into hand-wide scaling. [[card:132989|Twilight Tidehunter]] concentrates additional stats into the left-most Murloc in hand, while [[card:98948|Choral Mrrrglr]] converts that stored hand strength into combat stats.

The source finds an early Golden [[card:96786|Brann Bronzebeard]], then uses Murloc Battlecries and [[card:132883|Kelp Keeper]] to generate and repeat value while the spell-target engine comes online.

## When to commit

- You have Tidecaller or Tidehunter **and** a reliable stream of Tavern Spells that can target Murlocs.
- Brann plus useful Murloc Battlecries makes the transition much safer; the source explicitly rolls for Golden Brann and the new spell-scaling pieces.
- A hand payoff such as [[card:98509|Bream Counter]] or board conversion through Choral gives the scaling somewhere useful to land.

Do not force this from one isolated payoff card. The source begins with handbuff support, then commits only after Brann and repeatable spell targeting line up.

## How to play it

1. **Build the hand:** target Tidecaller/Tidehunter with useful Tavern Spells so the buffs spread through or concentrate in your hand.
2. **Double the value:** use Brann with Murloc Battlecries; Kelp Keeper can repeat a friendly Battlecry when the right target is worth the gold.
3. **Cycle actual Murlocs:** play and sell [[card:60028|Primalfin Lookout]], [[card:133075|Captain Cookie]], and spare [[card:131145|Mama Mrrglton]] copies when they improve discovery, hand quality, or Battlecry scaling. Keep one board slot open before starting the chain.
4. **Convert the hand:** keep Bream Counter growing and use Choral Mrrrglr to bring the hand's accumulated stats into combat.
5. **Finish the board:** [[card:126637|Expert Aviator]] and [[card:120677|Flighty Scout]] add hand-based combat utility after the raw scaling engine is established.

## Execution and traps

- Preserve a cycling slot. Full boards turn Primalfin and Battlecry chains into expensive hand clutter.
- Targeted Tavern Spells are the fuel; random expensive shop purchases are not a substitute.
- Plan the order before clicking. The source repeatedly runs short on recruit time once the gold and spell generation become effectively unbounded.
- Brann and Kelp Keeper are engine pieces, not sacred final-board units. Sell transitional value when the mature Murloc board needs the slot.

## Useful moments

- **06:28:** Tidecaller spell-to-hand scaling appears.
- **07:25:** Kelp Keeper, Golden Mama Mrrglton, and Golden Brann form the value shell.
- **14:28:** the source summarizes the loop as unlimited gold plus targeted pump spells.
- **20:30:** first clean mature Tavern board.
- **23:10:** strongest clean late Tavern board before the final combat.
