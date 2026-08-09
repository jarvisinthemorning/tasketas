---
title: Choose One Turbo Hogrider
slug: quilboar-choose-one-hogrider
season: 14
modes:
- solo
tribes:
- quilboar
tags:
- season 14
- choose one
- blood gems
- rally
core:
- 116195
- 116434
addons:
- 116190
- 132636
- 110664
cycle: []
board_examples:
- stage: mid
  turn: 10
  timestamp: 715
  note: The Choose One shell is fully online, with Turbo Hogrider and repeated Gem Rat choices feeding a broad Blood Gem board.
  units:
  - {card_id: 132632, slot: 1, attack: 51, health: 83}
  - {card_id: 132632, slot: 2, attack: 56, health: 91}
  - {card_id: 132636, slot: 3, attack: 95, health: 158}
  - {card_id: 116195, slot: 4, attack: 17, health: 29}
  - {card_id: 113154, slot: 5, attack: 26, health: 45}
  - {card_id: 116434, slot: 6, attack: 149, health: 89}
  - {card_id: 116434, slot: 7, attack: 61, health: 93}
- stage: end
  turn: 14
  timestamp: 1290
  note: The last stable Tavern board before the final combat, with the Choose One engine spread across two Turbo Hogriders while Gatekeeper Amalgam carries 2.4k/3.6k.
  units:
  - {card_id: 132632, slot: 1, attack: 1.5k, health: 2.2k}
  - {card_id: 116195, slot: 2, attack: 661, health: 960}
  - {card_id: 132636, slot: 3, attack: 1.9k, health: 2.8k}
  - {card_id: 116195, slot: 4, attack: 513, health: 746}
  - {card_id: 133329, slot: 5, attack: 2.4k, health: 3.6k, annotation: Divine Shield}
  - {card_id: 116434, slot: 6, attack: 496, health: 344, golden: true}
evaluation:
  version: 1
  assessed_at: '2026-08-09'
  classification:
    build_window: Midgame engine; late only with fuel
    setup_debt: Medium — Choose One generation must already exist
    execution: Medium — repeated casts, not full APM
  baseline:
    name: Minimal-fuel engine illustration
    model: hogrider-core-v1
    modeled_recruit_phases: 4
    parameters:
      hogriders: 1
      other_quilboars: 5
      choose_one_cards_per_turn: 1
      starting_gem_attack: 1
      starting_gem_health: 1
    assumptions:
    - One ordinary Turbo Hogrider and one Gem Rat
    - One Gem Day played each turn, alternating Attack and Health upgrades
    - Five other Quilboar receive each Hogrider Blood Gem
    - No Golden core, trinket, Discover chain, or additional Choose One generation
    interpretation: This separate four-phase illustration is not projected from the mature Turn 10 board. The demonstrated source trajectory also uses extra Choose One volume, additional Hogriders, upgraded Gems, and secondary engines.
  luck:
    tavern_tier: 6
    turns: 2
    simulations: 50000
    required_tribes: [quilboar]
    scenarios:
    - label: From scratch at Tavern 6
      required: [116434, 116195]
      owned: []
    - label: Gem Rat already owned
      required: [116434, 116195]
      owned: [116434]
    - label: Gem Rat owned; one rival holds Hogrider
      required: [116434, 116195]
      owned: [116434]
      held_by_rivals: 1
  external:
    firestone:
      url: https://www.firestoneapp.com/battlegrounds/comps
      comp_id: quilboar_choose_one
      power: 13.1
      average_position: 3.76
      tier: B
      difficulty: Medium
      games: 27621
      captured_at: '2026-08-09'
    hsreplay:
      url: https://hsreplay.net/battlegrounds/comps/88/quilboar-choose-one
      tier: A
      difficulty: Easy
      captured_at: '2026-08-09'
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/88/quilboar-choose-one
  comp_id: '88'
- type: firestone
  url: https://www.firestoneapp.com/battlegrounds/comps
  comp_id: quilboar_choose_one
source:
  type: youtube
  url: https://www.youtube.com/watch?v=d50H4G3vd58
  author: dogdog
video:
  id: d50H4G3vd58
  timestamp: 248
source_published_at: '2026-08-04'
verified_at: '2026-08-08'
---

## Game plan

Generate repeated Choose One cards with [[card:116434|Gem Rat]] and related effects, then let [[card:116195|Turbo Hogrider]] convert those casts into Blood-Gem scaling. [[card:132636|Jailbird Juggernaut]] is the source's primary Rally carry, while [[card:116190|Thorned Trailblazer]] adds more Choose One value.

[[card:110664|Felboar]] can consume shop stats in the demonstrated line, but the comp's identity is Hogrider plus Choose One volume—not generic Demon consumption.

## How to build it

- **Bridge:** collect Choose One generation without sacrificing basic board strength.
- **Commit:** the source calls Turbo Hogrider the scaler; without it, the package lacks a reliable ceiling.
- **Scale:** cast Choose One effects in the order that maximizes Gem production before moving stats.
- **Finish:** transfer accumulated Blood Gems into resilient final carries and keep Juggernaut positioned to Rally safely.

## Practical cautions

Do not spread permanent Gems across units you expect to sell. Delay transfers until the final carries are clear, but do not die holding a hand full of theoretical value.

The source's blunt warning is useful: miss Turbo Hogrider and this can become a very efficient route to eighth place. Treat the card as the commitment signal, not a hoped-for future miracle.

The late Tavern proof is much stronger than the earlier transition board: the source finishes with carries at 1.5k/2.2k, 1.9k/2.8k, and 2.4k/3.6k before winning. That is the payoff standard—not merely assembling the named pieces.
