---
title: Murlocs APM
slug: murlocs-apm
season: 14
patch: '36.2.0'
modes:
- solo
tribes:
- murloc
tags:
- season 14
- APM
- spells
- hand scaling
classification: meta
core:
- 96786
- 133026
addons:
- 103670
- 132883
- 122277
- 132989
- 130298
- 126637
- 108922
- 122219
- 98948
cycle:
- 103670
- 132883
- 122277
- 110400
packages:
- title: Core
  purpose: Brann multiplies Battlecry spell generation; Tidecaller turns every spell cast on a Murloc into hand-and-board scaling.
  badge: Required core
  optional: false
  cards: [96786, 133026]
- title: Targeted spell supply
  purpose: Generate cheap targeted casts with Oozeling, then retrigger its Battlecry with Kelp Keeper.
  badge: Optional — spell engine
  optional: true
  cards: [103670, 132883]
- title: Economy and card flow
  purpose: Keep the turn moving with doubled Battlecries, extra Murlocs, and premium spell value instead of spending the whole timer rolling.
  badge: Optional — APM fuel
  optional: true
  cards: [96786, 122277, 110400]
- title: Focus the hand carry
  purpose: Put the intended carry left-most in hand, then target Twilight Tidehunter while Tidecaller scales the rest of the Murlocs.
  badge: Optional — hand scaling
  optional: true
  cards: [132989, 133026, 130298]
- title: Pull from hand
  purpose: Aviator summons the highest-Attack hand minion; Forager does the same but only for a Murloc.
  badge: Optional — combat conversion
  optional: true
  cards: [126637, 108922]
- title: Late hand pieces
  purpose: Keep Bile Spitter as Venomous utility and let Choral gain the total stats of every minion still in hand.
  badge: Optional — late upgrades
  optional: true
  cards: [122219, 98948]
related_routes: []
composition_minions:
- {card_id: 96786, count: 1, golden_count: 0}
- {card_id: 133026, count: 1, golden_count: 0}
composition_spells: []
board_examples:
- stage: mid
  timestamp: 800
  phase: tavern
  image: /static/boards/murlocs-apm-core.webp
  note: A stable recruit turn with the scaling shell online and enough time left to decide which generated resources are worth cycling.
- stage: late
  timestamp: 1360
  phase: tavern
  image: /static/boards/murlocs-apm-late.webp
  note: A stable late Tavern state showing why hand payoffs and combat conversion matter after the spell loop has produced real scale.
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/67/murlocs-apm
  comp_id: '67'
source:
  type: youtube
  url: https://www.youtube.com/watch?v=Ppj60f3j_AE
  author: Shadybunny
video:
  id: Ppj60f3j_AE
  timestamp: 381
source_published_at: '2026-08-02'
verified_at: '2026-08-11'
---

## How it works

[[card:133026|Shamanic Tidecaller]] is the payoff: every spell cast on a Murloc buffs Murlocs in both hand and warband. [[card:96786|Brann Bronzebeard]] multiplies useful Battlecries; with [[card:103670|Oozeling Gladiator]], that means more Slimy Shields as cheap targeted casts. Actual Gold and card flow must come from the lobby's economy pieces, while [[card:132883|Kelp Keeper]] can retrigger Oozeling and [[card:130298|Balinda Stonehearth]] doubles spells that target friendly minions.

The source also demonstrates [[card:132989|Twilight Tidehunter]] as a focused hand scaler. Keep the intended carry left-most in hand, cast targeted spells on Tidehunter, and let Tidecaller scale the wider Murloc package at the same time. [[card:126637|Expert Aviator]] can summon the highest-Attack minion from hand for combat; [[card:108922|Diremuck Forager]] is restricted to the highest-Attack Murloc. [[card:98948|Choral Mrrrglr]] converts the stats of every minion remaining in hand into one board body at combat start.

This is an APM composition, but the loop is not literally infinite. Shadybunny's example receives exceptional extra Gold and a Golden Brann, then openly runs short on time. In an ordinary lobby, prioritize deterministic spell generation, clean hand order, and a finished combat board over squeezing every last action out of the turn.

The current HSReplay page was updated after the source video and shows a broader mature package: Magicfin, Balinda, Diremuck, Choral, Tidecaller, and Brann, with Bile Spitter as an add-on. The video directly teaches Golden Brann, Tidecaller, Twilight Tidehunter, targeted spells, and the hand-summon line. Treat the other directory pieces as current upgrades and conversion options rather than waiting for the complete six-card package before recognizing the engine.

## When to commit

- **Real signal:** Brann plus actual economy and [[card:133026|Shamanic Tidecaller]]. That matches the current HSReplay commit condition; neither card alone is the finished composition.
- **Good bridge:** [[card:103670|Oozeling Gladiator]] is cheap tempo before the pivot and becomes premium spell supply once Brann and Tidecaller are ready.
- **Hand route:** add [[card:132989|Twilight Tidehunter]] only when you can keep a meaningful hand carry left-most and repeatedly target Tidehunter.
- **Not enough:** a Tidecaller with no targeted spell supply, or Brann with no Battlecries and no Gold flow. Both leave you rolling for a combo rather than playing one.
- **Abort condition:** if the timer, hand space, or economy cannot support repeated casts, keep the strongest scaled Murlocs and convert to a simpler final board instead of forcing more APM.

## Shopping and sequencing

1. Build economy first. Brann must double Battlecries that actually create resources; buying him without useful Battlecries does not fund the loop.
2. Add Tidecaller when you can immediately cast spells on Murlocs. Each targeted cast should advance both the board and the hand rather than merely decorate one temporary unit.
3. Use Oozeling for two Slimy Shields, doubled by Brann. Trigger the Oozeling Battlecry again with Kelp Keeper when that produces more value than triggering a greedier but slower Battlecry.
4. Keep [[card:122277|Magicfin Mycologist]] when buying Tavern spells can create another Murloc carrying useful spell text. [[card:110400|Cloning Conch]] is premium card flow because it supplies two matching Murlocs without consuming several refreshes.
5. If using Twilight Tidehunter, move the intended permanent carry to the left-most hand slot before casting. Recheck the slot after every generated Murloc.
6. Add Aviator so the highest-Attack hand minion can fight without permanently occupying a board slot, or Forager when the intended summon is a Murloc. Leave board space for the temporary summon.
7. Use [[card:122219|Bile Spitter]] as a scalable Venomous hand target and late utility piece. Add Choral only once the hand contains enough total stats to justify a Tier 6 board slot.
8. Stop cycling early enough to field the combat pieces, restore the correct hand order, leave summon space, and position the warband. Unspent Gold is cheaper than entering combat with the engine in your hand.

## Positioning and traps

- **Left-most hand slot matters:** Twilight Tidehunter always buffs that slot. Generated Murlocs can silently change the intended recipient if you stop checking.
- **Highest Attack matters:** Aviator checks every minion in hand; Forager checks only Murlocs. A small ordering or buff mistake can summon the wrong body.
- **Leave space:** Aviator and Forager need an open board slot. A full board turns the hand carry into spectators with excellent stats and no ticket to the fight.
- **Keep Aviator back:** let earlier attacks create a board slot before Aviator's Rally checks for its summon; the source catches this positioning error at 16:21.
- **Protect the timer:** pre-plan the Oozeling/Kelp/target-spell sequence. The source repeatedly hits time pressure despite abundant Gold.
- **Balinda is acceleration, not the engine:** targeted spells remain necessary. Balinda does nothing for spells that do not target a friendly minion.
- **Do not overkeep generators:** once the hand and board are scaled, replace low-impact cycle pieces with actual combat conversion, Venomous utility, and Choral.
- **Do not copy the source economy:** the demonstrated Gold ceiling is unusually generous. The baseline route is Brann, Tidecaller, real spell supply, and disciplined execution.

## After a loss

- **The board stayed small:** Tidecaller arrived without enough targeted spells, or too many actions were spent rolling instead of casting.
- **The wrong hand minion grew:** Twilight Tidehunter's intended recipient was not left-most when the spell resolved.
- **The carry never appeared:** the board was full, another minion had higher Attack for Aviator, or another Murloc had higher Attack for Forager.
- **The turn ended unfinished:** the loop produced more decisions than the timer could support. Buy fewer speculative pieces and lock the final board earlier.
- **Choral disappointed:** too much scale had already moved onto the board, leaving insufficient total stats in hand for its Start of Combat payoff.
- **Brann occupied a dead slot:** there were not enough remaining Battlecries to justify keeping the economy engine over a combat unit.

## Useful timestamps

- **5:21** — The source identifies the Murloc pivot from a strong hand and Battlecry setup.
- **6:31** — Tidecaller appears and the plan becomes Brann, spells, and Murloc scaling.
- **7:30** — Compares the hand-scaling route with the Golden Brann APM route.
- **13:20** — Clean mid-game Tavern snapshot with the scaling shell established.
- **14:23** — Summarizes the loop: excess Gold, targeted spells, and a Golden hand payoff.
- **16:21** — Catches an Aviator positioning mistake caused by playing too quickly.
- **18:08** — Admits the economy exceeds what the timer can realistically spend.
- **22:40** — Clean late Tavern snapshot while the source again prioritizes targeted spells.
- **23:55** — Final source recap: the composition was enabled by Golden Brann.
