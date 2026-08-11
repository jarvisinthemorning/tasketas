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
packages:
- title: Commit
  purpose: Improve Blood Gems and bank one repeatable Choose One card each turn while both Quilboar routes remain open.
  badge: Commit signal
  optional: false
  cards: [116434]
- title: Core
  purpose: Let Bramble Tunneler generate repeatable Choose One cards, then convert every play into broad Blood Gem scaling with Hogrider.
  badge: Required core
  optional: false
  cards: [116195, 132632]
- title: Choose One
  purpose: Feed Hogrider with cheap choices, doubled effects, repeatable Rally generation, and a late whole-board payoff.
  badge: Shopping engine
  optional: false
  cards: [116182, 132630, 116190, 132632, 113154, 132634, 132929]
- title: Blood Gem quality
  purpose: Raise the value of every Hogrider trigger once Choose One generation is stable.
  badge: Scaling upgrades
  optional: true
  cards: [122566, 80755]
- title: Final carries
  purpose: Convert the broad spell-and-Gem economy into resilient bodies or an additional Rally threat.
  badge: Optional finishers
  optional: true
  cards: [132636, 133329, 110664]
related_routes:
- title: Gem Rat → Blood Golems
  slug: quilboar-bristlemane-juggernaut
  purpose: Switch when Juggernaut arrives with Bristlemane loading or repeatable Gem Confiscation before Turbo Hogrider.
  cards: [132320, 126671, 132636]
composition_minions:
- {card_id: 132632, count: 1, golden_count: 0}
- {card_id: 116195, count: 1, golden_count: 0}
- {card_id: 132636, count: 1, golden_count: 0}
- {card_id: 133329, count: 1, golden_count: 0}
- {card_id: 116434, count: 1, golden_count: 0}
composition_spells:
- {card_id: 116596, count: 1}
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
verified_at: '2026-08-11'
---

## Game plan

Use [[card:116434|Gem Rat]] as the soft commitment signal while both Quilboar routes remain open. [[card:132632|Bramble Tunneler]] then supplies repeatable Choose One cards through Rally, and [[card:116195|Turbo Hogrider]] converts every one you play into broad Blood-Gem scaling. [[card:132636|Jailbird Juggernaut]] is the source's primary Rally carry, while [[card:116190|Thorned Trailblazer]] adds more Choose One value.

[[card:110664|Felboar]] can consume shop stats in the demonstrated line, but the comp's identity is Hogrider plus Choose One volume—not generic Demon consumption.

## How to build it

- **Commit softly:** Gem Rat improves Blood Gems and banks a Gem Day every turn, but do not ignore an earlier Bristlemane/Juggernaut or Confiscation core.
- **Bridge:** collect the cards in the Choose One shopping section without sacrificing basic board strength.
- **Commit:** pair Turbo Hogrider with Bramble Tunneler. Hogrider provides the scaling payoff and Tunneler keeps generating the Choose One fuel that sustains it.
- **Scale:** cast Choose One effects in the order that maximizes Gem production before moving stats.
- **Finish:** transfer accumulated Blood Gems into resilient final carries and keep Juggernaut positioned to Rally safely.

## Practical cautions

Do not spread permanent Gems across units you expect to sell. Delay transfers until the final carries are clear, but do not die holding a hand full of theoretical value.

The source's blunt warning is useful: miss Turbo Hogrider and this can become a very efficient route to eighth place. Treat the card as the commitment signal, not a hoped-for future miracle.

The late Tavern proof is much stronger than the earlier transition board: the source finishes with carries at 1.5k/2.2k, 1.9k/2.8k, and 2.4k/3.6k before winning. That is the payoff standard—not merely assembling the named pieces.

If Juggernaut plus Bristlemane or repeatable Gem Confiscation appears before Turbo Hogrider, use the pivot panel above rather than forcing this route.
