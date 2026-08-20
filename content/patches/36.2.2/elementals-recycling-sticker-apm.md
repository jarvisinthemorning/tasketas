---
title: Elementals — Recycling Sticker APM
slug: elementals-recycling-sticker-apm
season: 14
patch: '36.2.2'
modes: [solo]
tribes: [elemental]
tags: [apm, shop-buff, scaling, trinket]
classification: highroll
core: []
addons: []
cycle: []
packages:
  - title: Commit
    purpose: Take this line only when Recycling Sticker is offered and you already have Elemental generation ready to turn its free Refreshes into a real cycle.
    badge: Commit signal
    optional: false
    cards: [120705]
  - title: Core
    purpose: Sticker makes each played Elemental refresh for free; Brann doubles Tavern Tempest so one buy supplies two more Elementals to keep the loop moving.
    badge: Required core
    optional: false
    cards: [120705, 64077, 96786]
  - title: Inflate the Tavern
    purpose: Air Revenant and En-Djinn stack permanent shop buffs while Sticker supplies the repeated Refreshes that cash them in.
    badge: Scaling engine
    optional: false
    cards: [126173, 126175]
  - title: Convert the stats
    purpose: Unbound Tempest copies the largest Tavern body every three Elementals; Mana Surge converts the same play volume into whole-board scaling.
    badge: Final carries
    optional: false
    cards: [132983, 120674]
  - title: Anti-scam finish
    purpose: Use Elemental of Surprise to secure a Golden Wildfire when Cleave is more valuable than another greedy generator.
    badge: Optional — anti-scam
    optional: true
    cards: [101280, 64189]
related_routes: []
composition_minions: [64077, 96786, 126173, 126175, 132983, 120674, 64189]
composition_spells: []
board_examples:
  - stage: late
    turn: 12
    timestamp: 824
    phase: tavern
    image: /static/boards/elementals-recycling-sticker-apm-late.webp
    note: The mature loop has converted a heavily inflated Tavern into multiple large carries while Brann remains available for more generation.
discovery_sources:
  - type: hsreplay
    url: https://hsreplay.net/battlegrounds/comps/37/elementals-stat-scaling-shop-buff/
    comp_id: '37'
supporting_sources: []
source:
  type: youtube
  url: https://www.youtube.com/watch?v=KZw3Q1U5gAU
  author: JeefHS
video:
  id: KZw3Q1U5gAU
  timestamp: 340
source_published_at: '2026-08-20'
verified_at: '2026-08-20'
---

## How it works

[[card:120705|Recycling Sticker]] turns every Elemental you play into a free Tavern Refresh. The loop becomes sustainable when [[card:96786|Brann Bronzebeard]] doubles [[card:64077|Tavern Tempest]], turning one Battlecry into two generated Elementals; each generated body triggers Sticker again when played.

The cycle does two scaling jobs at once. [[card:126173|Air Revenant]] repeatedly casts Easterly Winds as Gold is spent, and [[card:126175|En-Djinn Blazer]] adds another permanent Refresh payoff. Those shop buffs are finally converted by [[card:132983|Unbound Tempest]], which takes the stats of the highest-Health Tavern minion every three Elementals. [[card:120674|Unleashed Mana Surge]] is the complementary board-wide payoff.

This page is deliberately a **Highroll**, not the ordinary HSReplay Elemental route: the source's near-infinite version is built around a specific Greater Trinket and accelerated by Chenvaala. The underlying shop-buff composition is currently listed by HSReplay, but the showcased loop should not be presented as the normal floor.

## When to commit

- **2:52** is only a forecast: Jeef says the game is probably APM, but the defining engine is not assembled yet.
- At **3:41**, he deliberately keeps [[card:64077|Tavern Tempest]] for the coming Trinket choice.
- The mechanical commit is the [[card:120705|Recycling Sticker]] pick around **5:40**, immediately followed by the claim that the line can go infinite. Sticker without Elemental supply is not enough; Tempest plus [[card:96786|Brann Bronzebeard]] is what keeps feeding plays.
- Abort this exact line if Sticker is absent, or if you cannot find enough generation before spending the remaining Gold on low-impact Elementals. The normal shop-buff route may still be playable, but this source does not prove its ordinary floor.

## How to play the recruit turns

1. Preserve [[card:64077|Tavern Tempest]] for the Sticker turn instead of cashing it too early. With Brann, its Battlecry supplies two Elementals and therefore two more free Refresh triggers.
2. After Sticker is active, play an Elemental, take the free Refresh, and reassess. Do not buy every Elemental merely because the Refresh is free: Jeef rejects low-impact bodies at **3:17** and again at **5:33–5:38**.
3. Add permanent Tavern scaling before chasing final bodies. [[card:126173|Air Revenant]] and [[card:126175|En-Djinn Blazer]] make later Refreshes and buys worth more.
4. Convert the inflated shop with [[card:132983|Unbound Tempest]]. Three Elemental plays copy the highest-Health Tavern body's stats, so sequence the third trigger when the shop contains a suitably large target.
5. Keep [[card:120674|Unleashed Mana Surge]] when the board has enough Elementals to benefit from repeated whole-board buffs.
6. Watch the actual Gold total. At **13:53**, Jeef explicitly slows down because he has only a single Brann and does not want the loop to run dry. “Infinite” is the ceiling, not permission to stop counting.

## Positioning and traps

- Against scam boards, lead with [[card:64189|Wildfire Elemental]] so its overkill can remove adjacent utility bodies. Jeef cites an opponent's first-position Wildfire as smart at **1:13**, then prioritizes the Surprise–Wildfire finish over another Djinni at **8:56**.
- [[card:101280|Elemental of Surprise]] is a conversion tool, not generic scaling. Use it when tripling Wildfire materially improves the next combat; otherwise preserve the engine slots.
- Do not fill all seven slots with permanent carries too early. The loop needs room to play and sell generated Elementals, and Brann must remain while Tavern Tempest is the main supply engine.
- Do not treat the Turn 12 board or five-figure [[card:132983|Unbound Tempest]] as typical. Chenvaala, Recycling Sticker, the generated Elemental chain, and the source's successful hits all contribute to that ceiling.

## Useful timestamps

- **2:52** — Jeef forecasts an APM Elemental game.
- **3:41** — Tavern Tempest is held specifically for the upcoming Trinket.
- **5:40** — Recycling Sticker is selected; this is the actual mechanical commit.
- **8:07** — The Elemental loop is described as effectively infinite.
- **8:24–8:59** — Anti-scam planning leads to Wildfire over another Djinni.
- **11:38** — Jeef calls Recycling Sticker the reason the engine is guaranteed to keep refreshing.
- **13:44** — Stable late Turn 12 Tavern view of the mature board and heavily buffed shop.
- **13:53–13:57** — He slows the cycle to avoid running out of Gold with only one Brann.
