---
title: Demons Shop Buff
slug: demons-shop-buff
season: 14
modes:
- solo
tribes:
- demon
tags:
- season 14
- shop buff
- consume
- spells
classification: meta
core:
- 132901
- 132899
- 130298
- 110664
addons:
- 130662
- 72060
- 96786
cycle: []
packages:
- title: Commit
  purpose: Stay only after persistent shop buffs meet a real consumer; Distractor alone is not a Demon comp.
  badge: Buffed shop + consumer
  optional: false
  cards: [132901, 130662]
- title: Core
  purpose: Buff the Tavern through targeted spells, generate Madness, double those spells, then consume the enlarged shop.
  badge: Required core
  optional: false
  cards: [132901, 132899, 130298, 110664]
- title: Shop scaling
  purpose: Keep targeting Distractor to grow future shops; Ashen Corruptor adds temporary shop stats when self-damage is already supported.
  badge: Build the buffet
  optional: false
  cards: [132901, 121687]
- title: Madness package
  purpose: Generate Methodical Madness with Imp-lusionist, then use Balinda to double targeted spells and keyword gains.
  badge: Spells + keywords
  optional: false
  cards: [132899, 132903, 130298]
- title: Consumers
  purpose: Turn the enlarged Tavern into permanent bodies through Fodder, spell casts, Demon plays, or direct Madness consumption.
  badge: Convert shop into stats
  optional: false
  cards: [130662, 110664, 72060, 132903]
- title: Economy and safety
  purpose: Brann supplies the Battlecry economy needed for long turns; Soul Rewinder protects self-damage lines.
  badge: Keep the engine moving
  optional: true
  cards: [96786, 100949]
- title: Final carries
  purpose: Keep several large Demons and add useful keywords instead of leaving one enormous, naked scam target.
  badge: Spread stats and keywords
  optional: true
  cards: [130662, 72060, 110664]
related_routes: []
composition_minions:
- {card_id: 132901, count: 1, golden_count: 0}
- {card_id: 132899, count: 1, golden_count: 0}
- {card_id: 130298, count: 1, golden_count: 0}
- {card_id: 110664, count: 1, golden_count: 0}
- {card_id: 130662, count: 1, golden_count: 0}
composition_spells:
- {card_id: 132903, count: 1}
board_examples:
- stage: mid
  turn: 10
  timestamp: 545
  phase: tavern
  image: /static/boards/demons-shop-buff-mid.webp
  note: The pivot is online but the board still contains replaceable support; use this as the point where shop scaling starts becoming a real composition.
- stage: late
  turn: 14
  timestamp: 1210
  phase: tavern
  image: /static/boards/demons-shop-buff-late.webp
  note: A clean late Tavern state showing why the line wants several consumers and protected carries rather than one pile of stats.
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/41/demons-shop-buff
  comp_id: '41'
source:
  type: youtube
  url: https://www.youtube.com/watch?v=7dFLg3c2GxA
  author: Shadybunny2
video:
  id: 7dFLg3c2GxA
  timestamp: 322
source_published_at: '2026-08-11'
verified_at: '2026-08-11'
---

## How it works

[[card:132901|Devilish Distractor]] makes every spell cast on it permanently improve future Tavern minions. [[card:132899|Imp-lusionist]] supplies [[card:132903|Methodical Madness]], which turns that shop investment into permanent Demon stats and useful keywords. [[card:130298|Balinda Stonehearth]] doubles targeted friendly spells, while [[card:110664|Felboar]], [[card:72060|Insatiable Ur'zul]], and [[card:130662|Twisted Wrathguard]] provide different ways to consume the enlarged shop.

The source begins on a different route and explicitly refuses to commit from one Distractor. The Demon pivot becomes credible only after a Golden [[card:96786|Brann Bronzebeard]] and [[card:130662|Twisted Wrathguard]] create the economy and consumption needed to exploit the shop. That is the useful lesson: build the line the game offers, not the line named on the guide.

## When to commit

- **Not enough:** one [[card:132901|Devilish Distractor]] with no reliable consumer. Spending Gold on permanent shop buffs is wasted if the final board cannot eat those stats.
- **Real signal:** persistent shop scaling plus [[card:130662|Twisted Wrathguard]], [[card:110664|Felboar]], [[card:72060|Insatiable Ur'zul]], or repeatable [[card:132903|Methodical Madness]].
- **Strong accelerator:** [[card:96786|Brann Bronzebeard]] and good Battlecry economy give you enough actions to roll, buy, sell, and keep feeding Wrathguard's future Refreshes.
- **Stay flexible:** the source keeps a functioning alternative line until the Demon engine actually appears. Do the same; do not sell a board for a future shop that may never arrive.

## Shopping and sequencing

1. Secure a consumer before sinking repeated spells into [[card:132901|Devilish Distractor]].
2. Target Distractor with useful spells so the permanent Tavern buff is attached to actions you already wanted to take.
3. Use [[card:132899|Imp-lusionist]] to generate [[card:132903|Methodical Madness]]. Keep enough hand space for both copies when its Deathrattle resolves.
4. Add [[card:130298|Balinda Stonehearth]] once targeted spells are plentiful enough for the double cast to matter.
5. With [[card:130662|Twisted Wrathguard]], sell low-value minions to seed later Refreshes with Fodder. With Felboar, plan spell casts in groups of three. With Ur'zul, cycle Demons without sacrificing the final board.
6. Spend Madness on the Demons you intend to keep, especially when the Tavern offers defensive keywords that convert raw stats into combat value.
7. Once several carries are large, use the remaining Gold on economy and matchup tech instead of greedily making the shop even larger.

## Positioning and traps

- Distractor is an investment, not a carry by itself. If you cannot consume the shop soon, preserve tempo and stay on another route.
- [[card:132899|Imp-lusionist]] needs to die, and its generated cards need hand space. A full hand can erase the payoff.
- [[card:130298|Balinda Stonehearth]] doubles targeted friendly spells; buying it without enough useful targets is expensive decoration.
- [[card:130662|Twisted Wrathguard]] rewards selling, but frantic cycling can leave the final board short on bodies or time. Decide which Demons are permanent before the last seconds.
- One gigantic Demon is vulnerable to scam. The source deliberately spreads keywords and stats, and later declines a greedier triple when it would make the board easier to counter.
- [[card:100949|Soul Rewinder]] belongs only when self-damage is part of the line. It does not advance ordinary shop scaling by itself.

## After a loss

- **The shop was huge but the board was small:** you bought scaling before securing enough consumers.
- **The comp never started:** you treated Distractor as the commitment signal instead of waiting for the paired engine.
- **Madness generation fizzled:** Imp-lusionist survived, or your hand was too full for its Deathrattle.
- **Your biggest Demon disappeared:** stats were concentrated without enough keywords, protection, or a second carry.
- **The turn timed out:** Brann economy and Wrathguard selling created more actions than you could sequence. Pick permanent carries first, then cycle.
- **You lost to a comparable stat board:** stop investing in a larger future Tavern and spend the final turns on matchup-specific defense.

## Useful timestamps

- **5:22** — Why one Distractor is not enough to commit to Demons.
- **6:34** — Golden Brann and Wrathguard open the pivot.
- **7:51** — The source explains why the engine is now playable after staying flexible.
- **9:05** — Clean Turn 10 Tavern snapshot after the pivot.
- **12:48** — A harder shop-scaling turn comes together.
- **16:22** — The source starts replacing greed with final-fight utility.
- **20:10** — Clean late Tavern state before the final combat.
