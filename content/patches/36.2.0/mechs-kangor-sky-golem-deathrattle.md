---
title: 'Mechs Deathrattle: Kangor–Sky Golem'
slug: mechs-kangor-sky-golem-deathrattle
season: 14
patch: '36.2.0'
modes:
- solo
tribes:
- mech
tags:
- season 14
- deathrattle
- resurrection
- scaling
- late-game pivot
classification: meta
core:
- 59935
- 130798
addons:
- 97408
- 120025
- 61930
- 98592
- 112364
- 96812
- 90425
cycle: []
packages:
- title: Commit
  purpose: Take the line when Kangor can resurrect an already-meaningful Falling Sky Golem and your Deathrattle history or repeatable triggers will keep growing future Golems.
  badge: Scaled Golem + Kangor
  optional: false
  cards: [59935, 130798]
- title: Core
  purpose: Grow Falling Sky Golem through Deathrattle history, then use Kangor to resurrect plain copies of the first two Mechs that die.
  badge: Required core
  optional: false
  cards: [59935, 130798]
- title: Deathrattle amplifier
  purpose: Titus accelerates Golem scaling and repeats Kangor's resurrection when its board slot produces more combat value than another carry.
  badge: Optional — double the triggers
  optional: true
  cards: [97408]
- title: Magnetic summon package
  purpose: Auto Assembler on Deflect-o-Bot turns summoned Automatons into repeated Divine Shield resets while adding more Deathrattles to the game history.
  badge: Optional — secondary combat engine
  optional: true
  cards: [120025, 61930]
- title: Magnetic supply and protection
  purpose: Scrap Scraper generates attachments; Prosthetic Hand gives a key Mech Reborn, while Annoy-o-Module adds Divine Shield and Taunt where combat ordering needs them.
  badge: Optional — build resilient carries
  optional: true
  cards: [98592, 112364, 96812]
- title: Matchup utility
  purpose: Buy Leeroy only when removing one opposing carry matters more than another engine or scaling slot.
  badge: Optional — utility, not core
  optional: true
  cards: [90425]
related_routes:
- title: Mechs Magnetics
  slug: mechs-magnetics
  purpose: Route into the broader Magnetic line when Spark Snapper plus repeatable supply is the real signal and Kangor cannot reliably refill with scaled Sky Golems.
  cards: [132676, 98592, 132312]
composition_minions:
- {card_id: 59935, count: 1, golden_count: 0}
- {card_id: 130798, count: 2, golden_count: 0}
- {card_id: 97408, count: 1, golden_count: 0}
- {card_id: 61930, count: 1, golden_count: 0}
composition_spells: []
board_examples:
- stage: late
  turn: 12
  timestamp: 854
  phase: tavern
  image: /static/boards/mechs-kangor-sky-golem-deathrattle-late.webp
  note: A Turn 12 Tavern view of the mature protected board, with multiple triple-digit carries and the support slots visible before combat.
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/68/mechs-deathrattle/
  comp_id: '68'
source:
  type: youtube
  url: https://www.youtube.com/watch?v=KjKTgeAppVI
  author: Shadybunny2
video:
  id: KjKTgeAppVI
  timestamp: 451
source_published_at: '2026-06-30'
verified_at: '2026-08-13'
---

## How it works

[[card:130798|Falling Sky Golem]] keeps a permanent count of your triggered Deathrattles wherever it is and converts each trigger into +4/+2. That means the setup starts before the final board exists: ordinary Deathrattles, [[card:98592|Scrap Scraper]], and [[card:120025|Auto Assembler]] all make later Golems larger. The source finds Golem at 7:29 and immediately treats the accumulated history as safety rather than as a fresh, unscaled Tier 6 body.

[[card:59935|Kangor's Apprentice]] is the second half of the identity. Its Deathrattle summons plain copies of the first two Mechs that died that combat. Engineer the death order so scaled Golems or another valuable Mech occupy those resurrection slots; at 16:21 Shadybunny explicitly says that Sky Golems are what he wants in Kangor. “Plain copies” means attachments are not copied, but Falling Sky Golem's wherever-this-is scaling still gives the summoned copy its accumulated history.

[[card:97408|Titus Rivendare]] amplifies both halves: more Deathrattle triggers grow every Golem faster, and an extra Kangor trigger produces another resurrection wave. It is powerful rather than sacred. At 15:13 the source considers whether Titus is worth its slot in the mirror, so do not preserve it automatically when another carry or matchup tool would win more combat.

The source's other engine is a support package, not the reason to enter this composition. [[card:120025|Auto Assembler]] magnetized onto [[card:61930|Deflect-o-Bot]] summons Automatons in combat, repeatedly restoring Deflect-o-Bot's Divine Shield. [[card:98592|Scrap Scraper]] keeps generating Magnetic material. This package gives the board a functional floor when Kangor does not immediately hit the ideal resurrection wave, but a lobby offering Spark Snapper and Magnetic duplication more readily than Kangor/Golem should follow the related **Mechs Magnetics** route instead.

## Pivot signal

- **Hold pieces; do not call it a comp yet:** Kangor can preserve favorable Mech death history, and a Golem can be a strong standalone carry, but either card alone is only direction.
- **Commit:** field [[card:59935|Kangor's Apprentice]] with an already-meaningful [[card:130798|Falling Sky Golem]], or with enough repeatable Deathrattles that Golem will become meaningful quickly. You must also be able to make the Golem one of the first two Mechs to die.
- **What is not enough:** an unscaled Golem plus no Deathrattle density; a Kangor whose first deaths are disposable Mechs; or Titus without worthwhile Deathrattles.
- **Source signal:** Kangor is bought at 4:51 while death order is being shaped, but the honest commitment arrives at 7:29–7:35 when Golem appears and the existing Deathrattle history makes it immediately valuable.
- **Expectation check:** Teron Gorefiend, Fridge Magnet, Arch-Mage's Perch, and Magician's Top Hat accelerate the showcased game. They raise its supply and ceiling; they do not create the Kangor–Golem interaction. The source still finishes second and calls it a below-average Mech game, so copy the engine, not its exact stat pace.

## Composition recipe

1. **Resurrection anchor:** one Kangor. Golden is excellent but not required.
2. **Preferred first deaths:** one or two scaled Falling Sky Golems. Reborn can make a Golem harder to remove and can add another useful body, but preserve the intended first-two-Mech death order.
3. **Amplifier slot:** Titus when doubling Golem growth and Kangor's refill is worth the board space.
4. **Secondary carry:** Deflect-o-Bot carrying one or more Auto Assembler Deathrattles so in-combat Mech summons reset its shield.
5. **Flexible slots:** another protected carry, a Deathrattle generator, or matchup utility. Leeroy belongs here, never in the mandatory engine.

This is a recipe rather than a seven-card lock. Magnetize Auto Assemblers onto the Deflect-o-Bot carry instead of reserving board slots for every support card. Shop toward two dangerous resurrection targets and enough independent combat value that one disrupted Kangor does not end the fight.

## Shopping and sequencing

1. Trigger useful Deathrattles while searching Tier 6; every trigger improves all present and future Falling Sky Golems.
2. Buy Kangor only with a credible Mech death plan. Track the **first two** friendly Mechs to die, not simply the two largest Mechs on the starting board.
3. Use Scrap Scraper when hand space can receive its generated Magnetic cards. Titus doubles the trigger, not your hand capacity.
4. Put Auto Assembler on Deflect-o-Bot when the Automaton summons will create repeated shield resets. This is a complete secondary package even when the Kangor wave is imperfect.
5. Add Reborn deliberately. At 10:16–10:32 the source avoids magnetizing onto Golem in a way that would compromise its Reborn value while explaining that the board will scale Golems faster.
6. Reassess Titus and utility every opponent. Leeroy at 21:54 is a matchup purchase after the engine is built, not evidence that it belongs in Core.

## Positioning and traps

- **Control the first deaths.** Taunt, attack order, and Reborn all change Kangor's resurrection pool. If two low-value Mechs die first, a huge Golem dying third is too late.
- **Do not attach everything to a Golem automatically.** Kangor returns plain copies, and the source explicitly protects Reborn utility rather than blindly adding Magnetics to Golem.
- **Do not expose Kangor before its targets die.** Its Deathrattle is only valuable after the intended first deaths are recorded.
- **Protect Titus when its extra triggers matter, but sell the slot when they do not.** The source's mirror discussion demonstrates that amplification has an opportunity cost.
- **Avoid a single-plan board.** The Deflect-o-Bot/Auto Assembler “clown car” can win fights where resurrection is disrupted; conversely, raw Magnetic stats without the Kangor/Golem interaction are better taught by the related route.
- **Do not grade ordinary games against the source's accelerants.** Hero power, trinkets, and free economy materially speed its board, while the engine itself remains reproducible from Tavern-pool cards.

## After a loss

- **Kangor summoned weak Mechs:** your first-two death order was wrong; add Taunt or reposition the bodies that must die first.
- **Golem was too small:** you found Tier 6 without enough earlier or repeatable Deathrattle triggers.
- **The refill never happened:** Kangor died too early, was silenced, or did not have board room when its Deathrattle resolved.
- **Titus felt like dead weight:** its extra trigger did not outweigh the carry or utility minion occupying the same slot.
- **Deflect-o-Bot lost its shield once and stayed exposed:** you lacked in-combat Mech summons, or Auto Assembler was not attached to a body that died in time.
- **The showcased numbers looked unreachable:** discount Teron's exact-copy resummon, Fridge Magnet generation, and the trinket economy before judging your baseline board.

## Useful timestamps

- **4:30–5:06** — Shapes which Mechs die and buys Kangor at 4:51; useful death-pool setup before the line is complete.
- **7:29–7:35** — Finds Falling Sky Golem and says it makes the position safe: the clearest commitment moment.
- **8:29–8:50** — Searches Tier 6 for more Golems while developing the shared Mech support.
- **9:20–9:28** — Takes Titus and taunts the Deathrattle that must die.
- **10:16–10:32** — Declines a Magnetization that would compromise Golem's Reborn value and explains faster Golem scaling.
- **11:36–12:49** — Adds Reborn and Auto Assemblers while Scrap Scraper continues supplying Magnetics.
- **14:13** — Clean Turn 12 Tavern inspection of the mature protected board and multiple triple-digit carries.
- **15:13–15:24** — Questions Titus's board-slot value in the mirror; evidence that it is an amplifier, not mandatory Core.
- **16:21–16:25** — Explicitly identifies Sky Golems as the desired Kangor resurrection targets.
- **17:02–17:22** — Explains the Deflect-o-Bot summon-and-shield-reset support package.
- **21:30–21:42** — Golden Kangor resolves after Titus dies; the resurrection wave wins a low-percentage combat.
- **21:54–22:14** — Considers and buys Leeroy strictly as matchup utility.
- **23:32–23:56** — Finishes second and describes the run as a below-average Mech game, crediting the Deflect-o-Bot adaptation.
