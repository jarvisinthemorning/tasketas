---
title: Utility Drone Magnetics
slug: mech-utility-drone-magnetics
season: 14
modes:
- solo
tribes:
- mech
tags:
- season 14
- magnetic
- end of turn
- generation
core:
- 98588
- 132895
addons:
- 132676
- 132312
cycle: []
board_examples:
- stage: early
  turn: 8
  timestamp: 452
  note: The Tavern shell before the final Mech engine appears, with Balinda already carrying the board while the player looks for the transition.
  units:
  - card_id: 126916
    slot: 1
    attack: 3
    health: 5
  - card_id: 110321
    slot: 2
    attack: 12
    health: 6
    golden: true
    annotation: Divine Shield
  - card_id: 126916
    slot: 3
    attack: 8
    health: 15
  - card_id: 122342
    slot: 4
    attack: 4
    health: 4
  - card_id: 113635
    slot: 5
    attack: 5
    health: 5
    annotation: Divine Shield
  - card_id: 130298
    slot: 6
    attack: 32
    health: 54
- stage: mid
  turn: 9
  timestamp: 565
  note: Golden Glambot is online at triple-digit stats, but the board is still a mixed transition shell rather than the finished Utility Drone composition.
  units:
  - card_id: 126916
    slot: 1
    attack: 3
    health: 5
  - card_id: 110321
    slot: 2
    attack: 18
    health: 6
    golden: true
    annotation: Divine Shield
  - card_id: 126916
    slot: 3
    attack: 8
    health: 15
  - card_id: 122342
    slot: 4
    attack: 10
    health: 10
  - card_id: 130298
    slot: 5
    attack: 32
    health: 54
  - card_id: 132893
    slot: 6
    attack: 112
    health: 132
    golden: true
    annotation: Divine Shield
- stage: end
  turn: 14
  timestamp: 1269
  note: The last Tavern turn before the winning combat, with Golden Glambots and Utility Drones converting the end-of-turn engine into five-digit carries.
  units:
  - card_id: 101314
    slot: 1
    attack: 2
    health: 10
    golden: true
  - card_id: 130298
    slot: 2
    attack: 38
    health: 60
    golden: true
  - card_id: 132893
    slot: 3
    attack: 13k
    health: 13k
    golden: true
  - card_id: 132893
    slot: 4
    attack: 33k
    health: 33k
    golden: true
    annotation: Divine Shield
  - card_id: 120905
    slot: 5
    attack: 10
    health: 20
  - card_id: 98588
    slot: 6
    attack: 4.8k
    health: 4.8k
  - card_id: 98588
    slot: 7
    attack: 12k
    health: 12k
    golden: true
    annotation: Divine Shield
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/2/mechs-magnetics
  comp_id: '2'
composition_minions:
- {card_id: 132893, count: 1, golden_count: 0}
- {card_id: 120905, count: 1, golden_count: 0}
- {card_id: 98588, count: 1, golden_count: 0}
- {card_id: 130298, count: 1, golden_count: 0}
- {card_id: 101314, count: 1, golden_count: 0}
composition_spells:
- {card_id: 104472, count: 1}
source:
  type: youtube
  url: https://www.youtube.com/watch?v=EhDY7nt7obg
  author: dogdog
video:
  id: EhDY7nt7obg
  timestamp: 492
source_published_at: '2026-08-06'
verified_at: '2026-08-08'
---

## Game plan

Use [[card:132895|Rescue Bot]] as the tempo bridge and Magnetic generator, then transition into [[card:98588|Utility Drone]]. Every attached Magnetic increases the value of Utility Drone's end-of-turn scaling, so generation and attachment count matter more than buying random large Mechs.

[[card:132676|Spark Snapper]] and [[card:132312|Drone Duplicator]] help assemble the premium engine. The source specifically warns that Spark Snapper is not automatically useful for every Mech interaction; buy it for the line it actually enables.

## How to build it

- **Bridge:** Rescue Bot gives bodies and resources while you level.
- **Commit:** Utility Drone plus reliable Magnetic generation is the real breakpoint.
- **Scale:** attach Magnetics to permanent carries and multiply the generator pieces when Goldenizer effects appear.
- **Finish:** retain enough generation to keep scaling, but replace obsolete bridge pieces once the final board is secure.

## Positioning and traps

Spread important utility across more than one body when combat allows it. Do not magnetize everything onto a fragile target that can be neutralized by one Venomous hit.

The source's late board reaches extreme stats only after several premium pieces are assembled. A lone Utility Drone is direction, not permission to greed yourself into eighth.
