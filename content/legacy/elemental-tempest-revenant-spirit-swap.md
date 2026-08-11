---
title: Tempest–Revenant Spirit-Swap APM
slug: elemental-tempest-revenant-spirit-swap
season: 14
modes: [solo]
tribes: [elemental]
tags: [APM, scaling, tavern-stats, hero-specific]
core: [132983, 126173, 71464]
addons: [120705, 132207, 133453]
cycle: [64038, 64040, 119951, 64189]
composition_minions:
  - {card_id: 132983, count: 1, golden_count: 0}
  - {card_id: 126173, count: 1, golden_count: 0}
composition_spells: []
composition_prerequisites:
  - {card_id: 71464, count: 1}
board_examples: []
source:
  type: youtube
  url: https://www.youtube.com/watch?v=KRm5_T4KuA0
  author: JeefHS
video:
  id: KRm5_T4KuA0
  timestamp: 668
source_published_at: '2026-08-09'
verified_at: '2026-08-10'
---

## Description

[[card:126173|Air Revenant]] turns Gold spending into Easterly Winds, so every later refresh can grow Tavern bodies. [[card:132983|Unbound Tempest]] converts that Tavern scaling into permanent warband stats after every three Elementals played.

The source's extreme version uses [[card:71464|Spirit Swap]] to lend the highest-Health Tavern body the Attack of an already-large friendly minion before Tempest copies the Tavern body's full stats. Jeef shows the line reaching about **205k Attack on Turn 13**, then visible **1M and 2M Attack** Tempests on Turn 14.

## When to commit

- You already have [[card:132983|Unbound Tempest]] plus [[card:126173|Air Revenant]], or a credible Tavern-6 route into both.
- You are playing [[card:71464|Spirit Swap]] and can preserve a large friendly Attack value to move into the Tavern.
- You have enough health and economy to play Elementals in groups of three instead of buying isolated stats.

Do not force this from Air Revenant alone. Jeef only pivots after the Pirate route stops producing Hooktusks, then explicitly identifies the Revenant APM line as the necessary alternative.

## Enablers

- [[card:132207|Admiration]] is the source's preferred Dark Gift and adds another way to convert a neighboring giant into combat stats; random Dark Gift odds are not included in the model.
- [[card:133453|Living Prison]] is a source-shown one-off conversion: Activate it before buying a giant Tavern minion so Prison gains that minion's stats.
- A large existing attacker gives Spirit Swap something meaningful to copy into the Tavern immediately.

## How to play

1. Spend at least 7 Gold after finding Air Revenant so Easterly Winds becomes active.
2. Refresh while cycling Elementals; active Winds build a high-Health Tavern anchor.
3. Use Spirit Swap between your largest attacker and that Tavern anchor. The swap itself is temporary, so sequence it immediately before triggering Tempest.
4. Play Elementals in exact groups of three. Each Unbound Tempest then permanently gains the highest-Health Tavern minion's full stats; Golden Tempest gains double.
5. Repeat the loop. Keep Tempests and Revenant, and sell temporary Elementals rather than sacrificing an engine slot.

## Cycle and temporary pieces

The source's [[card:120705|Recycling Sticker]] turns each Elemental played into a free refresh, connecting the Tempest counter directly to Tavern growth. Source-shown fuel includes [[card:64038|Sellemental]], [[card:64040|Water Droplet]], and [[card:119951|Glowing Cinder]]. [[card:64189|Wildfire Elemental]] advances the counter too, but becomes a retained cleave payoff once its Attack is large enough.

## Failure modes

- Spending Gold without refreshing wastes much of Easterly Winds' persistent value.
- Triggering Tempest before Spirit Swap leaves the Tavern anchor with Health but little Attack.
- Holding too many permanent support units chokes the buy–play–sell loop.
- The million-stat ceiling depends on Spirit Swap, accumulated Tavern scaling, repeated three-Elemental triggers, and a very specific high-roll. The deterministic score deliberately models a bounded version, not the video's 2M outcome.

## Useful timestamps

- **11:08** — Jeef identifies the Revenant APM line and says Admiration makes it especially strong.
- **13:36** — the failed Hooktusk route makes the Elemental pivot necessary.
- **15:20** — visible three-Elemental counting begins during the APM loop.
- **18:01** — the board reaches roughly 205k Attack.
- **19:51** — the Turn 14 Tavern board visibly reaches 1M and 2M Attack.
