---
title: Primitive Painter Murloc Cycle
slug: murloc-primitive-painter-cycle
season: 14
modes:
- solo
tribes:
- murloc
tags:
- season 14
- low-tier cycle
- board scaling
- apm
core:
- 122281
- 131145
addons: []
cycle: []
board_examples:
- stage: mid
  timestamp: 874
  note: Golden Primitive Painter is online and every cheap cycle card is turning into permanent Murloc stats.
  units:
  - {card_id: 122277, slot: 1, attack: 41, health: 48}
  - {card_id: 108922, slot: 2, attack: 102, health: 109}
  - {card_id: 122281, slot: 3, attack: 106, health: 115, golden: true, annotation: Taunt}
  - {card_id: 108922, slot: 4, attack: 80, health: 81}
  - {card_id: 133283, slot: 5, attack: 110, health: 117}
  - {card_id: 133283, slot: 6, attack: 102, health: 101}
- stage: late
  timestamp: 1040
  note: A useful late-game Tavern board showing the same Painter shell after several more low-tier cycles; the following combat is not a win.
  units:
  - {card_id: 122277, slot: 1, attack: 266, health: 270}
  - {card_id: 108922, slot: 2, attack: 179, health: 193}
  - {card_id: 122281, slot: 3, attack: 180, health: 191, golden: true, annotation: Taunt}
  - {card_id: 108922, slot: 4, attack: 156, health: 157}
  - {card_id: 133283, slot: 5, attack: 197, health: 205}
  - {card_id: 133283, slot: 6, attack: 174, health: 173}
source:
  type: youtube
  url: https://www.youtube.com/watch?v=7f4_AskT4Dk
  author: Christian 2
video:
  id: 7f4_AskT4Dk
  timestamp: 644
source_published_at: '2026-08-05'
verified_at: '2026-08-08'
---

## Game plan

[[card:122281|Primitive Painter]] rewards every Tavern Tier 3-or-lower card played by scaling the Murloc board. That changes the shopping rule: cheap, playable cards are engine fuel rather than filler.

The source starts moving toward Murlocs, discovers Painter, reads its low-tier trigger, and then explicitly searches for cheaper Murlocs. [[card:131145|Mama Mrrglton]] supplies a useful Murloc body while the cycle develops.

## How to build it

- **Bridge:** keep low-tier Murlocs that can be played efficiently rather than clogging the hand.
- **Commit:** Painter plus enough cheap card flow is the signal.
- **Scale:** play Tier 3-or-lower cards before spending gold on expensive units that do not trigger Painter.
- **Finish:** turn the final board into durable Murloc bodies while preserving one cycling slot for continued triggers.

## Practical cautions

Do not confuse “cheap” with “free.” A low-tier card that destroys your economy or forces out a real carry is still a bad buy.

This line is intentionally different from Kelp Keeper/Brann spell-target APM: Painter cares about the Tavern tier of cards played, not repeatedly targeting one Murloc with Tavern Spells.
