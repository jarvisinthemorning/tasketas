---
title: Plaguerunner Portrait Butchering Loop
slug: undead-plaguerunner-butcher-loop
season: 14
modes: [solo]
tribes: [undead]
tags: [season 14, trinket, deathrattle, attack scaling, cycle]
core: [133391, 126451, 120104]
addons: [133712, 130884, 120219, 97408, 132322, 133081]
cycle: [110412]
composition_minions: []
composition_spells: []
board_examples:
  - stage: end
    turn: 14
    timestamp: 885
    note: Last Tavern turn before the verified first-place combat. Six permanent Undead have reached roughly 940 Attack while Cataclysmic Harbinger remains as spell-copy support.
    units:
      - {card_id: 126451, slot: 1, attack: 938, health: 342}
      - {card_id: 130884, slot: 2, attack: 28, health: 30}
      - {card_id: 120219, slot: 3, attack: 936, health: 341}
      - {card_id: 120219, slot: 4, attack: 938, health: 342}
      - {card_id: 133081, slot: 5, attack: 957, health: 363, annotation: Divine Shield}
      - {card_id: 120104, slot: 6, attack: 941, health: 347}
      - {card_id: 120104, slot: 7, attack: 939, health: 356, annotation: Divine Shield}
source:
  type: youtube
  url: https://www.youtube.com/watch?v=8d42ovfpwBw
  author: BeterBabbit
video:
  id: 8d42ovfpwBw
  timestamp: 388
source_published_at: '2026-08-08'
verified_at: '2026-08-09'
---

## Description

[[card:133391|Plaguerunner Portrait]] turns every outside-combat destruction of [[card:126451|Plaguerunner]] into another plain copy. Feed that copy to [[card:110412|Butchering]]: Butchering permanently gives all your Undead +5 Attack, Plaguerunner's outside-combat Deathrattle adds another +4 Attack, and the Portrait puts the Plaguerunner back in hand so the next Butchering can do it again.

[[card:120104|Drustfallen Butcher]] supplies the first fuel through Avenge. [[card:133712|Sphere of Memory]] and [[card:130884|Cataclysmic Harbinger]] then copy the last Tavern spell cast, so ending the turn on Butchering creates the large refill shown in the source. The loop is repeatable rather than literally limitless: each repetition still needs a generated or copied Butchering.

[[card:120219|Friendly Geist]] adds the second scaling layer. Its Deathrattle permanently increases the Attack granted by Tavern spells, and [[card:97408|Titus Rivendare]] accelerates that bank while the Geist package is active.

## When to commit

Commit when you have Plaguerunner Portrait and can pair its Plaguerunner with Drustfallen Butcher. The Portrait alone preserves the sacrifice target, but without a steady Butchering supply it produces only occasional bursts rather than a scaling engine.

## Enablers

- Drustfallen Butcher converts friendly combat deaths into Butchering spells for the following recruit phase.
- Sphere of Memory makes two copies of the last Tavern spell cast each turn; Butchering must remain the last spell.
- Cataclysmic Harbinger adds another end-of-turn copy of the last Tavern spell.
- Friendly Geist and Titus Rivendare permanently raise the Attack granted by future Tavern spells.
- [[card:132322|Dead Bellringer]] provides another outside-combat Plaguerunner destruction while feeding the Reborn package.
- [[card:133081|Barrier Banshee]] gives the attack-heavy board a health and Divine Shield payoff while Reborn effects are firing.

## How to play

1. Keep enough disposable or Reborn Undead to trigger Drustfallen Butcher's Avenge repeatedly in combat.
2. If Sphere of Memory or Cataclysmic Harbinger is active, make Butchering the last Tavern spell cast so the correct spell is copied.
3. During recruit, cast each banked Butchering on Plaguerunner—not on a permanent carry.
4. Let the Portrait return a plain Plaguerunner after every sacrifice, then replay that copy for the next Butchering.
5. Use Dead Bellringer on Plaguerunner when available for another outside-combat Deathrattle and Reborn trigger.
6. Preserve stronger combat bodies while the repeated global buffs turn the whole Undead board into threats.

## Cycle and temporary pieces

Butchering is the consumed resource: each copy destroys Plaguerunner and applies its own permanent +5 Attack buff. Plaguerunner is the reusable target because its Deathrattle gains the outside-combat bonus and the Portrait immediately replaces it.

## Failure modes

- Sacrificing the wrong Undead breaks the Portrait refund and can delete a real carry.
- A board that cannot trigger Drustfallen Butcher's Avenge enters the next recruit phase without enough Butchering fuel.
- Casting another Tavern spell after Butchering makes Sphere of Memory and Cataclysmic Harbinger copy the wrong resource.
- The engine is heavily attack-weighted; without health, Divine Shield, Reborn, or utility, large numbers can still trade badly into scam.
- Hand space matters because the generated Butcherings and returned Plaguerunner compete for room.

## Demonstrated payoff

The final Turn 14 recruit board shows six permanent Undead between 936 and 957 Attack, plus Cataclysmic Harbinger as spell-copy support. The following combat wins the lobby. The result is large, repeatable board-wide attack scaling rather than a single lucky combat summon.

## Useful timestamps

- **6:28** — The Plaguerunner Portrait refund loop is online.
- **8:20** — Multiple Butchering spells are banked for the next recruit cycle.
- **14:45** — Clean final Turn 14 recruit board demonstrates the permanent payoff.
- **15:19** — The following combat converts the board into first place.
