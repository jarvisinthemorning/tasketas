---
title: Undead Attack Scaling
slug: undead-snazzy-reborn
season: 14
modes:
- solo
tribes:
- undead
tags:
- season 14
- attack scaling
- butchering
- reborn
- stat transfer
core:
- 120104
- 110412
- 95265
addons:
- 120219
- 130298
- 115610
- 95263
- 108992
- 132322
- 133083
- 133081
- 97408
cycle:
- 120104
- 95265
- 110412
packages:
- title: Commit
  purpose: Commit when Butcher has real summon volume and an existing Undead attack bridge. Butcher by itself is not a comp.
  badge: Butcher + bodies
  cards:
  - 120104
  - 95265
  - 126451
  - 122229
- title: Core
  purpose: Handless plus its Reborn Hand supplies three deaths, filling Butcher's Avenge (3). Butchering then builds permanent Attack across every Undead and future summon.
  badge: Required engine
  cards:
  - 120104
  - 110412
  - 95265
- title: Butchering amplification
  purpose: Trigger Geist before later casts, use Titus to multiply its Deathrattle, and add Balinda so targeted Butchering casts twice.
  badge: Improve every cast
  cards:
  - 120219
  - 97408
  - 130298
  - 110412
- title: Summon quality
  purpose: Handless fills Avenge efficiently; Striker and Summoner turn the permanent Attack bank into extra combat bodies instead of one fragile board.
  badge: Better deaths
  cards:
  - 95265
  - 115610
  - 95263
- title: Reborn conversion
  purpose: Handless creates a Reborn Hand, Summoner starts with Reborn, Bellringer forces an immediate Tavern return, and Mummifier supplies combat returns. Snazzy converts every trigger.
  badge: Tavern + combat
  cards:
  - 95265
  - 95263
  - 132322
  - 108992
  - 133083
- title: Defensive payoff
  purpose: Banshee converts repeated Reborn triggers into Health and Divine Shields. If Banshee itself has Reborn, Taunt forces its own return while Snazzy feeds the right-most recipient.
  badge: Survive the swing back
  cards:
  - 133081
  - 133083
related_routes:
- slug: undead-plaguerunner-butcher-loop
  title: Plaguerunner Portrait Butchering Loop
  purpose: A trinket variation where Portrait refunds every Plaguerunner destroyed outside combat; its commitment gate, recruit loop, and hand management are different enough to deserve their own guide.
  cards:
  - 133391
  - 126451
  - 120104
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/14/undead-attack-scaling
  comp_id: '14'
composition_minions:
- {card_id: 108992, count: 1, golden_count: 0}
- {card_id: 132322, count: 1, golden_count: 0}
- {card_id: 120104, count: 1, golden_count: 0}
- {card_id: 133083, count: 2, golden_count: 0}
- {card_id: 133081, count: 2, golden_count: 0}
composition_spells:
- {card_id: 110412, count: 1}
board_examples:
- stage: mid
  turn: 11
  timestamp: 787
  note: The attack bank is already online, but the board is still transitional. Balinda amplifies targeted spells, Snazzy has a right-most Banshee recipient, and Butcher continues producing Butchering.
  units:
  - {slot: 1, card_id: 95261, attack: 197, health: 6}
  - {slot: 2, card_id: 95263, attack: 193, health: 1}
  - {slot: 3, card_id: 121508, attack: 189, health: 5}
  - {slot: 4, card_id: 130298, attack: 16, health: 10}
  - {slot: 5, card_id: 133083, attack: 191, health: 8}
  - {slot: 6, card_id: 120104, attack: 191, health: 9}
  - {slot: 7, card_id: 133081, attack: 656, health: 474, annotation: Divine Shield}
- stage: late
  turn: 15
  timestamp: 1340
  note: This is a Ve'nari high-roll, not the baseline. Reborn Butcher and double Snazzy convert shop-phase sacrifices into enormous right-side bodies while two Banshees supply the defensive ceiling.
  units:
  - {slot: 1, card_id: 108992, attack: 400, health: 24}
  - {slot: 2, card_id: 132322, attack: 409, health: 30, annotation: Reborn}
  - {slot: 3, card_id: 120104, attack: 2.5k, health: 2.1k, annotation: Reborn}
  - {slot: 4, card_id: 133083, attack: 401, health: 29, annotation: Reborn}
  - {slot: 5, card_id: 133083, attack: 401, health: 29, annotation: Reborn}
  - {slot: 6, card_id: 133081, attack: 12k, health: 12k, annotation: Reborn · Divine Shield}
  - {slot: 7, card_id: 133081, attack: 3.6k, health: 3.2k, annotation: Reborn · Divine Shield}
source:
  type: youtube
  url: https://www.youtube.com/watch?v=gVDdCE_xjaQ
  author: Sevel
video:
  id: gVDdCE_xjaQ
  timestamp: 478
source_published_at: '2026-08-10'
verified_at: '2026-08-11'
---

## What this composition actually is

This is the general [[card:120104|Drustfallen Butcher]] Undead route, not the trinket-specific Plaguerunner loop. It layers three systems:

1. **Permanent Attack:** combat deaths generate [[card:110412|Butchering]], which destroys one friendly Undead and gives every Undead +5 Attack for the rest of the game.
2. **More and better bodies:** [[card:95265|Handless Forsaken]], [[card:115610|Deathly Striker]], and [[card:95263|Eternal Summoner]] turn that global Attack bank into repeated combat summons.
3. **Reborn conversion:** [[card:133083|Snazzy Phantom]] reads the returning unit's Attack and gives that much Attack and Health to your right-most Undead, while [[card:133081|Barrier Banshee]] supplies Health and Divine Shields.

That distinction matters. Butcher scales Attack very efficiently, but Attack alone still loses to Divine Shields, scam, and anything that survives the first hit. The summon and Reborn packages are what turn the number into a board.

## When to commit

Use the HSReplay signal literally: **attack scaling plus summons**.

- A Butcher alongside [[card:95265|Handless Forsaken]] or another reliable death chain is a real opening.
- An existing Undead midgame led by [[card:126451|Plaguerunner]] or [[card:122229|Dustbone Devastator]] makes the pivot safer because your later summons already inherit useful Attack.
- One naked Butcher with no bodies is not permission to hard-roll Tier 6. It is a 2/7 asking you to make several additional good decisions.
- A second Butcher is meaningful: the source takes the second copy at **7:58**, then levels because the spell engine is secured rather than because the final board is already complete.

## The recruit-turn loop

1. **Generate Butchering in combat.** Protect Butcher until at least three friendly deaths have occurred. Handless is particularly efficient: Handless dies, its summoned Hand dies, and the Reborn Hand dies again—three deaths for Butcher's Avenge (3).
2. **Improve future casts.** Trigger [[card:120219|Friendly Geist]] when practical; [[card:97408|Titus Rivendare]] multiplies the Deathrattle. Each trigger permanently improves the Attack granted by later Tavern spells.
3. **Use a real recruit-phase Reborn target.** [[card:95263|Eternal Summoner]] already has Reborn; destroying Handless can leave its Reborn Hand; and [[card:132322|Dead Bellringer]] forces an immediate Tavern return. [[card:108992|Mummifier]] belongs to the combat line and does not, by itself, prepare a recruit-phase Butchering target.
4. **Place the recipient last.** Snazzy always feeds your **right-most Undead**. Check the order before every Butchering; a utility swap can redirect an entire turn of stats.
5. **Cast Butchering on a Reborn Undead.** The spell grows every Undead, the target returns, and Snazzy gives the right-most recipient +X/+X equal to that returning unit's Attack.
6. **Use Balinda when available.** [[card:130298|Balinda Stonehearth]] makes spells that target friendly minions cast twice, so it directly amplifies Butchering rather than merely adding another body.

## Shopping priorities by job

- **Keep the engine fed:** second Butcher, Handless, and compact summon chains.
- **Improve every future spell:** Friendly Geist first; Titus if it produces enough extra Geist triggers to justify a slot.
- **Raise summon quality:** Deathly Striker and Eternal Summoner are the Tier 6 bodies that best exploit the permanent Attack bank.
- **Convert Reborn events:** Bellringer enables the Tavern line; Mummifier enables the combat line. Snazzy without actual returns is a premium-tier spectator.
- **Add defense:** Barrier Banshee. In the source it already has Reborn, so Taunt around **17:07** forces it to die, return, and participate in the chain.

## Positioning and resource traps

- **Right-most is functional.** Put the unit you want to keep permanently enormous in the final slot before triggering Reborn in the Tavern or combat.
- **Butcher needs three deaths before it pays you.** Do not place it where it gets removed before the summon chain starts.
- **Leave hand space.** Butcher produces spells and Deathly Striker produces Undead; a full hand silently deletes the value you built the composition around.
- **Do not overvalue raw Attack.** Banshee, Divine Shields, Reborn, and summon density are your answer to the composition's naturally thin Health.
- **Treat the source ceiling honestly.** Sevel's Turn 15 board uses Ve'nari and favorable Dark Gifts. The 12k/12k Banshee proves the interaction ceiling, not the average result of finding one Butcher.

## After a loss: diagnose the failure

- **No Butchering arrived:** Butcher died before Avenge (3), or the board did not produce enough friendly deaths.
- **The board had Attack but no staying power:** summon quality or Banshee arrived too late; you built a first-hit board rather than an Undead board.
- **Snazzy barely moved:** too few units actually returned with Reborn, or the intended recipient was not right-most.
- **A large unit was sacrificed without a payoff:** Snazzy copies the Attack of the unit when it is Reborn; it does not preserve every stat the unit had before dying.
- **The engine clogged:** spell generation or random Undead generation hit a full hand.
- **You died while rolling for Tier 6:** the real commit was never online. Butcher plus hope is still mostly hope.

## Why the Portrait loop remains separate

[[card:133391|Plaguerunner Portrait]] changes the economy and sequencing: destroying Plaguerunner outside combat refunds a plain copy, allowing repeated replay-and-sacrifice turns. That route uses Butchering, but its commitment gate, hand management, and recruit loop are specific enough to keep as a linked specialist guide rather than burying it inside the general composition.

## Source checkpoints

- **0:57:** Dustbone Devastator provides the early Undead attack bridge.
- **7:58:** the second Butcher secures the spell engine before leveling.
- **13:07:** Turn 11 shows Butcher, Balinda, Snazzy, and a right-most Banshee on the same online board.
- **16:14–17:17:** the source works through the Reborn/Snazzy technique and explicitly prioritizes Taunt on Banshee.
- **22:20:** the final fully readable Tavern board shows double Snazzy and double Banshee at the Ve'nari high-roll ceiling.
- **23:35:** the video returns to Recruit after the following combat, proving survival, but cuts before proving first place. The board is therefore labeled **Late game**, not “last turn before winning.”
