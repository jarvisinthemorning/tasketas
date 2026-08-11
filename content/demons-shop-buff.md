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
addons:
- 130662
- 130298
- 110664
- 72060
- 96786
cycle: []
packages:
- title: Commit
  purpose: There is no separate pre-Core signal; assemble Distractor and Imp-lusionist before treating this as the shop-buff composition.
  badge: No early commit
  optional: false
  cards: []
- title: Core
  purpose: Grow future Tavern minions with Distractor, then use Imp-lusionist's Madness to convert those shop stats and keywords.
  badge: Required core
  optional: false
  cards: [132901, 132899]
- title: Fodder economy
  purpose: Brann accelerates the buy-and-sell economy that keeps Wrathguard's future Refreshes stocked with Fodder.
  badge: Optional — demonstrated engine
  optional: true
  cards: [130662, 96786]
- title: Madness conversion
  purpose: Imp-lusionist generates Methodical Madness; Balinda can double the targeted spell and its shop-to-board conversion.
  badge: Optional — current Meta extension
  optional: true
  cards: [132899, 132903, 130298]
- title: Other consumers
  purpose: Felboar converts spell volume and Ur'zul converts Demon plays when either arrives before the full Madness package.
  badge: Optional — choose another payoff
  optional: true
  cards: [110664, 72060]
- title: Conditional support
  purpose: Ashen adds temporary shop stats only in a self-damage line; Soul Rewinder makes that damage safe.
  badge: Optional — self-damage only
  optional: true
  cards: [121687, 100949]
related_routes: []
composition_minions:
- {card_id: 132901, count: 1, golden_count: 0}
- {card_id: 132899, count: 1, golden_count: 0}
composition_spells: []
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

The minimum Tasketas engine is [[card:132901|Devilish Distractor]] plus [[card:132899|Imp-lusionist]]. Spells cast on Distractor permanently improve future Tavern minions; Imp-lusionist generates two [[card:132903|Methodical Madness]] spells to turn those shop stats and keywords into permanent Demon strength. There is no honest earlier commitment section—the two-card Core is the signal.

The linked Shadybunny game demonstrates a Wrathguard/Fodder alternative, with a Golden [[card:96786|Brann Bronzebeard]] supplying the economy to keep buying and selling. It also uses Imp-lusionist for Methodical Madness. The current HSReplay directory additionally lists [[card:130298|Balinda Stonehearth]] and [[card:110664|Felboar]] in its Core package, with [[card:72060|Insatiable Ur'zul]], [[card:121687|Ashen Corruptor]], and [[card:100949|Soul Rewinder]] as add-ons. Those rows are current-Meta extensions supported by their card text, not choices attributed to Shadybunny's game.

The source begins on a different route and explicitly refuses to commit from one Distractor. Its Demon pivot becomes credible only after Golden Brann and [[card:130662|Twisted Wrathguard]] create an alternative economy and conversion route. The useful lesson is the same: build the line the game offers, not the line named on the guide.

## When the Core is real

- **Not enough:** one Distractor without Imp-lusionist or another immediate way to convert the future shop.
- **Core assembled:** Distractor plus Imp-lusionist gives you both persistent shop scaling and repeatable Madness conversion.
- **Madness support:** [[card:130298|Balinda Stonehearth]] upgrades the spell route, but it is not part of the minimum Core.
- **Fodder alternative:** Wrathguard plus Brann-supported economy can open the demonstrated route instead of waiting for the Madness package.
- **Other alternatives:** [[card:110664|Felboar]] or [[card:72060|Insatiable Ur'zul]] can consume an already-buffed Tavern, but neither makes every optional package mandatory.
- **Stay flexible:** keep a functioning board until the full engine actually appears; do not sell everything for a future shop that may never arrive.

## Shopping and sequencing

1. Assemble Distractor and Imp-lusionist before treating this as the shop-buff composition.
2. Target Distractor with useful spells so its permanent Tavern scaling is attached to actions you already wanted to take.
3. Leave hand space for both Methodical Madness copies when Imp-lusionist's Deathrattle resolves.
4. Spend Madness on Demons you intend to keep, especially when the Tavern offers defensive keywords that convert raw stats into combat value.
5. Add Balinda only when targeted spells are plentiful enough for the double cast to matter.
6. If the Fodder route appears instead, use Battlecry economy to buy and sell deliberately without running out of board or hand space.
7. Felboar and Ur'zul are alternative consumers; do not wait for every package. Once several carries are large, spend the remaining Gold on matchup tech rather than a greedier future Tavern.

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
