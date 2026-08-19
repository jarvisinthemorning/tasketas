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
- 132207
cycle: []
packages:
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
- title: Felboar spell consumption
  purpose: Spell volume activates Felboar to consume the inflated Tavern; Balinda accelerates targeted-spell volume when those casts already have good targets.
  badge: Optional — current Meta consumer
  optional: true
  cards: [110664, 132901, 130298]
- title: Admiration ceiling
  purpose: Place each gifted recipient immediately right of the largest carry so Admiration adds that left neighbor's stats at Start of Combat.
  badge: Source highroll — Dark Gift required
  optional: true
  cards: [110664, 132207]
- title: Ur'zul consumer
  purpose: Ur'zul converts Demon plays when it arrives before the full Madness or Felboar package.
  badge: Optional — alternative payoff
  optional: true
  cards: [72060]
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
- stage: late
  turn: 12
  timestamp: 899
  phase: tavern
  image: /static/boards/demons-shop-buff-admiration-felboar.webp
  note: A clean late Recruit-phase view of the Gift-gated Admiration/Felboar ceiling; its scale is not an ordinary expectation for the Meta Core.
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/41/demons-shop-buff
  comp_id: '41'
supporting_sources:
- type: youtube
  url: https://www.youtube.com/watch?v=JX8sAmT5NSU
  author: dogdog
  label: Felboar consume engine with stacked Admiration Dark Gifts
  timestamp: 899
- type: youtube
  url: https://www.youtube.com/watch?v=WdmTggS98Lo
  author: BeterBabbit
  label: Magic Fan spell supply into Felboar and stacked Admiration ceiling
  timestamp: 623
source:
  type: youtube
  url: https://www.youtube.com/watch?v=7dFLg3c2GxA
  author: Shadybunny2
video:
  id: 7dFLg3c2GxA
  timestamp: 322
source_published_at: '2026-08-11'
verified_at: '2026-08-19'
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

## Admiration ceiling

[[card:110664|Felboar]] is a normal alternative consumer for a spell-heavy, inflated Tavern. After every three spells it consumes a Tavern minion and gains its stats; Golden Felboar gains double. This lets Distractor scaling and ordinary spell volume become permanent board strength without waiting for Madness.

[[card:132207|Admiration]] is not normal access. It is a Dark Gift that gives its recipient the stats of the minion immediately to its left at Start of Combat. The supporting source stacks several copies around already-large Felboars, so treat that result as a Gift-gated ceiling:

1. Preserve enough spell volume to activate Felboar in groups of three.
2. Grow the Tavern before each consume whenever the sequencing does not waste useful casts.
3. Spread permanent stats across at least two carries before adding more greed.
4. If Admiration appears, place each recipient immediately right of the carry whose stats it should gain.
5. Recheck every adjacency after a sell, tech substitution, or final-board reorder.

Admiration adds combat-start stats; it does not improve Felboar's consume cadence. Multiple copies are exceptional Gift access, and the source's final numbers are not an ordinary Felboar result.

The BeterBabbit supporting game reaches the same ceiling through Malcolm, Splinter Twin and Magic Fan. Fan supplies extra spells for Felboar's three-cast cadence while repeated Admiration Gifts inflate the final combat board. Those hero, trinket and Gift hits explain the showcase; the ordinary transferable package remains a buffed Tavern, sufficient spell volume, and Felboar as the consumer.

## Positioning and traps

- Distractor is an investment, not a carry by itself. If you cannot consume the shop soon, preserve tempo and stay on another route.
- [[card:132899|Imp-lusionist]] needs to die, and its generated cards need hand space. A full hand can erase the payoff.
- [[card:130298|Balinda Stonehearth]] doubles targeted friendly spells; buying it without enough useful targets is expensive decoration.
- [[card:130662|Twisted Wrathguard]] rewards selling, but frantic cycling can leave the final board short on bodies or time. Decide which Demons are permanent before the last seconds.
- One gigantic Demon is vulnerable to scam. The source deliberately spreads keywords and stats, and later declines a greedier triple when it would make the board easier to counter.
- [[card:100949|Soul Rewinder]] belongs only when self-damage is part of the line. It does not advance ordinary shop scaling by itself.
- Admiration reads the minion immediately to its left. A single misplaced tech card can turn the Gift from a giant copy into expensive confetti.
- Do not wait for Admiration before building Felboar. The transferable package is Tavern scaling plus three-spell consume cycles; the Gift is merely the absurd hat on top.

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
- **Admiration source 8:00** — transition shop with Felboar support pieces available.
- **Admiration source 14:59** — stable mature Tavern state with the Gift-gated carry structure online.
- **Admiration source 18:01** — combat evidence for the two-carry endpoint; not used as the publication crop because effects obscure the board.
- **BeterBabbit 10:30** — the Magic Fan/Wrathguard cycle is online and the Felboar route starts converting spell volume.
- **BeterBabbit 19:23** — the final combat exposes the stacked-Admiration ceiling; do not treat its roughly 20,000-stat scale as normal.
