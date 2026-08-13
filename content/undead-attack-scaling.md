---
title: Undead Attack Scaling
slug: undead-attack-scaling
season: 14
modes:
- solo
tribes:
- undead
tags:
- season 14
- attack scaling
- reborn
- summons
classification: meta
core:
- 95265
- 120104
- 133083
addons:
- 122229
- 126451
- 120219
- 130298
- 108992
- 132322
- 133081
- 95263
- 115610
- 97408
cycle: []
packages:
- title: Commit
  purpose: Commit only when Drustfallen Butcher's permanent Attack has enough summons and Reborn bodies to use it; Handless is the cleanest partner.
  badge: Attack scaling + summons
  optional: false
  cards: [95265, 120104]
- title: Core
  purpose: Butcher raises every Undead's Attack, Handless supplies Reborn summons, and Snazzy converts each Reborn into stats on the right-most Undead.
  badge: Required core
  optional: false
  cards: [95265, 120104, 133083]
- title: Attack scaling
  purpose: Build permanent Attack first; Geist improves Tavern spells, Butcher supplies Butchering, and Balinda can double targeted casts.
  badge: Optional — scaling upgrades
  optional: true
  cards: [122229, 126451, 120219, 120104, 110412, 130298]
- title: Reborn and summons
  purpose: Add repeatable Reborn and bodies so the Attack scaling becomes combat value instead of a board of fragile glass cannons.
  badge: Optional — trigger supply
  optional: true
  cards: [108992, 132322, 95265, 95263, 115610]
- title: Payoffs and multipliers
  purpose: Banshee becomes a protected carry, Snazzy turns Reborn Attack into right-most stats, and Titus multiplies useful Deathrattles.
  badge: Optional — late upgrades
  optional: true
  cards: [133081, 133083, 97408, 130298]
- title: Mummifier reset loop
  purpose: Bellringer destroys a Reborn Mummifier; Mummifier's Deathrattle gives Bellringer Reborn, and Butchering Bellringer resets its Activate for another cycle.
  badge: Optional — execution package
  optional: true
  cards: [108992, 132322, 110412, 133083]
related_routes: []
composition_minions:
- {card_id: 95265, count: 1, golden_count: 0}
- {card_id: 120104, count: 1, golden_count: 0}
- {card_id: 133083, count: 1, golden_count: 0}
composition_spells: []
board_examples:
- stage: mid
  timestamp: 834
  phase: tavern
  image: /static/boards/undead-attack-scaling-mid.webp
  note: The Undead shell is established, but several slots are still replaceable while the Reborn payoff comes together.
- stage: late
  timestamp: 1260
  phase: tavern
  image: /static/boards/undead-attack-scaling-late.webp
  note: A stable late Tavern state showing the mature split between Reborn triggers, scaling pieces, and protected payoff bodies.
- stage: late
  turn: 12
  timestamp: 722
  phase: tavern
  image: /static/boards/undead-attack-scaling-mummifier-loop.webp
  note: A clean Recruit-phase view immediately before the repeated Mummifier and Bellringer reset sequence is demonstrated.
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/14/undead-attack-scaling
  comp_id: '14'
supporting_sources:
- type: youtube
  url: https://www.youtube.com/watch?v=Lx0X-QmruhM
  author: JeefHS
  label: Full Mummifier and Bellringer reset-loop demonstration
  timestamp: 719
- type: youtube
  url: https://www.youtube.com/watch?v=kboObgosKSQ
  author: JeefHS
  label: Short Mummifier loop explainer
  timestamp: 0
source:
  type: youtube
  url: https://www.youtube.com/watch?v=JGU9TeaO6VE
  author: Shadybunny
video:
  id: JGU9TeaO6VE
  timestamp: 436
source_published_at: '2026-08-01'
verified_at: '2026-08-11'
---

## How it works

[[card:120104|Drustfallen Butcher]] generates [[card:110412|Butchering]], which destroys one friendly Undead and permanently raises the Attack of every Undead this game. [[card:95265|Handless Forsaken]] supplies a Reborn summon, while [[card:133083|Snazzy Phantom]] turns every friendly Reborn into stats for your right-most Undead. The result is a board with very high global Attack plus one or more payoff bodies that also gain Health or protection.

The scaling has two layers. [[card:122229|Dustbone Devastator]], [[card:126451|Plaguerunner]], Butcher, and Butchering raise Undead Attack; [[card:120219|Friendly Geist]] improves the Attack granted by Tavern spells for the rest of the game. [[card:130298|Balinda Stonehearth]] can double friendly-targeted spells, while Reborn providers create the combat events that Snazzy and [[card:133081|Barrier Banshee]] reward.

Shadybunny's source demonstrates the route with [[card:121558|Maw Caster Portrait]], a trinket that refunds out-of-combat destruction with Gold. That economy helps the example explode, but it is not part of the baseline Meta Core. The current HSReplay directory also lists Deathly Striker, Friendly Geist, Balinda, and Snazzy in its Core package. Treat those as later upgrades around the minimum Butcher, Handless, and Snazzy engine rather than waiting for the complete directory board.

## When to commit

- **Real signal:** [[card:120104|Drustfallen Butcher]] plus actual summon/Reborn density, preferably [[card:95265|Handless Forsaken]]. This matches the directory's practical signal: Attack scaling plus summons.
- **Not enough:** one Butcher on a board with no bodies to die, no Reborn plan, and no useful Undead shell. Global Attack alone leaves you with fragile minions and poor combat conversion.
- **Good bridge:** Dustbone Devastator and Plaguerunner can preserve an Undead midgame while you look for Butcher and the Tier 6 payoffs.
- **Core online:** add [[card:133083|Snazzy Phantom]] once you can reliably trigger Reborn. Keep the intended permanent recipient as the right-most Undead.
- **Abort condition:** if you reach the late game with Attack but no repeatable summons, Reborn, or durable payoff, stop buying future scaling and preserve the strongest board available.

## Shopping and sequencing

1. Keep useful Undead bodies while Dustbone Devastator, Plaguerunner, and Friendly Geist build permanent Attack.
2. Buy Butcher when you already have enough summons or Reborn bodies for its Avenge trigger. Do not treat an unsupported Butcher as the full composition.
3. Use Butchering on an Undead whose death advances the board or whose board slot you are ready to replace; destroying an essential engine piece just for +5 Attack can lose more than it gains.
4. Add [[card:108992|Mummifier]] and [[card:132322|Dead Bellringer]] to spread Reborn. Prioritize Reborn on bodies that produce another useful summon or repeatable payoff.
5. Add Snazzy only when Reborn can trigger consistently, then keep the intended carry as the right-most Undead before combat.
6. [[card:133081|Barrier Banshee]] is a natural protected payoff because Reborn events rebuild its Divine Shield and add stats.
7. Use [[card:97408|Titus Rivendare]] only when doubling Friendly Geist, Handless Forsaken, Mummifier, or another useful Deathrattle earns the board slot. Titus does not multiply Snazzy's non-Deathrattle trigger.
8. Add Balinda when targeted spells—especially Butchering—are frequent enough to justify a Tier 6 support slot. Do not wait for every optional card before improving the final board.

## Mummifier reset loop

This is an optional execution package once [[card:108992|Mummifier]], [[card:132322|Dead Bellringer]], [[card:110412|Butchering]], and enough Gold are available. It does not replace the ordinary Butcher/Reborn Core.

1. **Activate Bellringer on Mummifier.** Mummifier gains Reborn, is destroyed, and returns. Its Deathrattle gives Bellringer Reborn.
2. **Cast Butchering on Bellringer.** Bellringer dies, returns through Reborn, and its Activate is available again. Butchering also adds the permanent Undead Attack.
3. **Repeat while resources justify it.** Each pass creates two Reborn events for Snazzy—one from Mummifier and one from Bellringer—while adding another Butchering layer.
4. **Keep the recipient right-most.** The loop is only worth the clicks if [[card:133083|Snazzy Phantom]] sends those Reborn stats to the intended carry.

The full source produces roughly ten Activates and twenty Reborn events in a turn, but that ceiling depends on an exceptional supply of Butchering and Gold. In a normal game, count the spells you can actually cast before reserving both board slots.

## Positioning and traps

- **Right-most matters:** Snazzy always buffs the right-most Undead. Recheck the order after every buy, sell, Reborn setup, or temporary tech card.
- **Attack is not Health:** global Attack scaling creates glass cannons unless Reborn, summons, Divine Shield, or Snazzy conversion keeps bodies alive.
- **Protect Snazzy:** it must survive long enough to watch friendly minions Reborn. Do not expose it as an early attacker without a matchup-specific reason.
- **Banshee must participate:** Barrier Banshee only refreshes its protection after friendly Reborn events. The source deliberately considers Taunt and attack order so it can convert that protection into combat value.
- **Tripling can reduce triggers:** the source notes that two separate activations can be better than one Golden copy during the build-up. Triple only when the stronger text or board space is worth losing a second trigger body.
- **Hand and board space still matter:** summon engines, generated Undead, and Reborn setup compete for slots. Decide which scaling pieces are permanent before the turn becomes a small administrative crisis.
- **Do not copy the source ceiling:** Maw Caster Portrait supplied extra Gold after destruction. Without that trinket, expect fewer actions and prioritize the minimum engine over recreating every displayed piece.
- **Do not start the reset backwards:** Bellringer targets Mummifier first so Mummifier's Deathrattle grants Bellringer Reborn. Butchering an unprotected Bellringer simply deletes half the loop. A tiny sequencing error with admirably large consequences.

## After a loss

- **Everything had huge Attack and died immediately:** you scaled the tribe but missed Reborn, summons, Divine Shield, or Health conversion.
- **Snazzy buffed the wrong unit:** the intended carry was not the right-most Undead when Reborn triggered.
- **Butcher never generated enough spells:** you lacked deaths and summons to trigger Avenge consistently.
- **Butchering made the board weaker:** you destroyed a current engine piece before a replacement or payoff was ready.
- **The board ran out of slots:** too many support pieces survived after their job was done; keep the active Reborn engine and remove obsolete bridges.
- **The source looked much stronger:** subtract Maw Caster Portrait's destruction economy before comparing your ordinary-lobby ceiling.

## Useful timestamps

- **7:16** — The source commits to the Undead line after finding a real Reborn/Deathrattle shell.
- **9:16** — Identifies the need for more summon tokens and looks toward Snazzy Phantom.
- **11:29** — Uses Butchering while discussing the Snazzy payoff.
- **13:54** — Clean mid-game Tavern snapshot before Snazzy fully takes over the route.
- **15:24** — Explains how high Attack makes Snazzy's Reborn conversion much larger.
- **18:30** — Rechecks the Snazzy plan and catches a Reborn sequencing mistake.
- **21:00** — Clean late Tavern snapshot with the mature engine.
- **22:54** — Adjusts positioning to preserve the protected payoff before the final fight.
- **Jeef 3:14** — the Mummifier/Bellringer reset sequence is introduced before assembly.
- **Jeef 8:03** — confirms the package is set up and identifies repeated Butchering as its fuel.
- **Jeef 11:07** — Bellringer is identified as the best Butchering fuel.
- **Jeef 11:59** — the complete loop is demonstrated step by step.
- **Jeef 12:44** — explains the one-Gold cadence and two Snazzy Reborn triggers per pass.
- **Jeef 15:26** — closes the teaching segment and notes Balinda as a further ceiling.
