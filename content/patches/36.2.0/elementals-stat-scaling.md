---
title: Elementals — Stat Scaling
slug: elementals-stat-scaling
season: 14
patch: '36.2.0'
modes: [solo]
tribes: [elemental]
tags: [scaling, battlecry, cycling]
classification: meta
core: [119951, 120674, 132981, 96786]
addons: [117406, 101267, 132983, 64296, 63626, 126173, 133453]
cycle: [64038, 119949, 64042, 64077]
packages:
  - title: Commit
    purpose: A Cinder you can trigger, an Elemental board, and enough economy to keep cycling open the route; Cinder alone does not.
    badge: Commit signal
    optional: false
    cards: [119951]
  - title: Core
    purpose: Trigger Cinder's Deathrattle and Custodian's Rally, then let Mana Surge and Brann convert repeated Elemental plays into board stats.
    badge: Required core
    optional: false
    cards: [119951, 120674, 132981, 96786]
  - title: Elemental cycle
    purpose: Buy these efficient Elementals first to create extra bodies, free Refreshes, and repeatable Battlecries while triggering Mana Surge.
    badge: Shopping engine
    optional: false
    cards: [64038, 119949, 64042, 64077]
  - title: Nomi–Brann shop branch
    purpose: Nomi inflates Tavern Elementals; Brann and Tavern Tempest extend the cycle, then Unbound Tempest or Living Prison converts the strongest shop body into permanent stats.
    badge: Optional — demanding economy branch
    optional: true
    cards: [63626, 96786, 64077, 126173, 132883, 132983, 133453]
  - title: Scaling carries
    purpose: Keep the bodies that turn repeated plays, sells, or a buffed Tavern into permanent combat stats.
    badge: Optional — scaling carries
    optional: true
    cards: [64296, 117406, 101267, 132983]
related_routes: []
composition_minions: [119951, 120674, 132981, 96786, 117406, 101267, 132983]
composition_spells: []
board_examples:
  - stage: late
    turn: 15
    timestamp: 1109
    phase: tavern
    image: /static/boards/elementals-stat-scaling-late.webp
    note: A stable late Tavern turn showing the mature engine before another high-volume Elemental cycle.
  - stage: late
    turn: 15
    timestamp: 1120
    phase: tavern
    image: /static/boards/elementals-stat-scaling-nomi-brann.webp
    note: A clean late Recruit-phase view of the Nomi/Brann branch after the Tavern has been inflated and conversion bodies are online.
discovery_sources:
  - type: hsreplay
    url: https://hsreplay.net/battlegrounds/comps/37/elementals-stat-scaling
    comp_id: '37'
supporting_sources:
  - type: youtube
    url: https://www.youtube.com/watch?v=hWQIUBEHVCk
    author: dogdog
    label: Nomi–Brann economy branch with Golden Brann ceiling
    timestamp: 884
  - type: youtube
    url: https://www.youtube.com/watch?v=pjPRVGf2LTw
    author: JeefHS
    label: Nomi-first shop scaling with Air Revenant, Kelp Keeper and Unbound conversion
    timestamp: 329
source:
  type: youtube
  url: https://www.youtube.com/watch?v=urKD45-Agjw
  author: JeefHS
video:
  id: urKD45-Agjw
  timestamp: 203
source_published_at: '2025-07-04'
verified_at: '2026-08-19'
---

## How it works

The current route turns every Elemental play into several layers of permanent stats. [[card:120674|Unleashed Mana Surge]] gives your Elementals +4/+4 whenever you play an Elemental. You must trigger [[card:119951|Glowing Cinder]]'s Deathrattle before its permanent extra-Health effect exists; [[card:132981|Moat Custodian]] similarly needs its Rally trigger to improve future Elemental buffs. [[card:96786|Brann Bronzebeard]] makes the best Battlecry Elementals produce more economy or permanent scaling, so the same Gold creates more plays and larger buffs.

The JeefHS source demonstrates the same Cinder–Mana Surge cycling decision model and explicitly marks the Elemental commit point, but it predates the current Season 14 card package. The current HSReplay video API no longer links a gameplay video for comp 37; this source's own description preserves the exact comp-37 URL, so it is used as historically associated strategy evidence rather than represented as a current directory link. In that recording Mana Surge used an older three-target version and the late economy came from older Deathrattle generators. The packages above therefore use the **current** HSReplay Core and current card text rather than pretending the video played Moat Custodian or today's exact Mana Surge.

## When to commit

- Treat [[card:119951|Glowing Cinder]] plus a healthy Elemental midgame and real cycle economy as the early signal.
- The current directory's full commitment condition is [[card:120674|Unleashed Mana Surge]] + [[card:96786|Brann Bronzebeard]] + established stat scaling. That is the point where cheap Elementals stop being ordinary tempo buys and become repeated board buffs.
- Do not force the line from Cinder alone. If you cannot keep buying and playing Elementals, the permanent quality upgrade has too little volume to matter.

## Recruit-turn sequence

1. Preserve board space before buying. The engine needs a free slot to play and sell Elementals repeatedly.
2. Prioritize [[card:64038|Sellemental]] for two plays from one purchase, [[card:64042|Refreshing Anomaly]] for free Refreshes, and [[card:64077|Tavern Tempest]] for another Elemental. With Brann, the Battlecries create substantially more fuel.
3. Play scaling Battlecries such as [[card:119949|Sand Swirler]] before the rest of the cycle so every later Elemental benefits.
4. Keep [[card:120674|Unleashed Mana Surge]] on board while cycling; selling the payoff to squeeze in one extra body defeats the route.
5. Only add [[card:132983|Unbound Tempest]] when your economy is already strong and you can keep the Tavern buffed. It is a payoff for sustained volume, not the card that creates the volume.

## Nomi–Brann shop branch

This optional branch uses [[card:63626|Nomi, Kitchen Nightmare]] to inflate Tavern Elementals before converting those shop stats into permanent bodies. It shares the guide's Brann and Elemental-cycle infrastructure but does not replace the directory-backed Cinder/Mana Surge Core.

1. **Start only with cycle volume.** Nomi needs enough Elementals to improve multiple future shops; buying it late with no generation is delayed optimism wearing a chef's hat.
2. **Use Brann with actual Battlecries.** [[card:64077|Tavern Tempest]] is the cleanest supply engine, while [[card:126173|Air Revenant]] can add more resources as Gold is spent. [[card:132883|Kelp Keeper]] can retrigger a useful Battlecry once per turn when that extra activation is worth its board slot.
3. **Convert the Tavern.** [[card:132983|Unbound Tempest]] repeatedly absorbs the highest-Health shop body after three Elemental plays. [[card:133453|Living Prison]] can instead absorb the next minion bought when that creates a better permanent carry.
4. **Sell Nomi when future shops stop mattering.** Once conversion pieces and cycle supply are established—or one more scaler blocks the combat board—cash out the Tavern quality instead of preserving it forever.

The source calls Golden Brann close to self-sustaining and questions whether ordinary Brann can compete in that exact line. Treat Golden Brann as the demonstrated ceiling, not the entry condition. “Infinite money” is shorthand: Gold, generated cards, hand and board space, animations, and the timer remain annoyingly finite.

The JeefHS supporting game proves that Nomi can be the primary scaling route rather than a late supplement, but Captain Sanders makes Golden Nomi unusually accessible. The transferable line is Nomi plus real Elemental supply and a way to convert the inflated Tavern; the hero-assisted Golden copy is ceiling, not Commit.

## Positioning and traps

- The source values economy generators before greed: without enough Gold or generated Elementals, you cannot find and repeatedly trigger the real engine.
- Lock the combat board before the timer expires. This route can spend an entire turn cycling and still lose because the final carry or utility card remained in hand.
- Do not keep every scaler. [[card:64296|Molten Rock]], [[card:117406|Meteorite Crasher]], and [[card:101267|Flourishing Frostling]] are possible carries, but board space is also an economic resource.
- Brann multiplies Battlecries; it does not double Mana Surge's non-Battlecry trigger. Buy it for Sand Swirler, Refreshing Anomaly, Tavern Tempest, and similar fuel—not as a second Mana Surge.
- If the engine cannot generate enough buys, stop chasing the high ceiling and preserve the strongest combat board you can field.
- Nomi buffs future Tavern Elementals; it does not directly scale the bodies already on your board. Do not keep cycling when the shop gains can no longer be converted before combat.

## After a loss

- **Committed too early:** you had Cinder but no Mana Surge, Brann, or sustainable Elemental supply.
- **Wrong shopping:** you rolled past Sellemental, Refreshing Anomaly, Sand Swirler, or Tavern Tempest while buying bodies that did not extend the cycle.
- **Board-space failure:** your carries filled every slot, so generated Elementals could not be played efficiently.
- **Timer failure:** the engine was online, but the turn ended before the final board was restored.
- **Unreachable ceiling:** the source's older Deathrattle economy was unusually strong; judge the current build by whether today's cycle is self-sustaining, not by the source's exact final numbers.

## Useful timestamps

- **3:23** — Jeef calls the Elemental commit point.
- **4:01** — He explains that Brann supplies enough Health scaling while Attack still needs support.
- **7:14** — He evaluates economy versus keeping Glowing Cinder.
- **13:23** — He explains why every Elemental play is now worth a large permanent stat gain.
- **18:29** — Stable late Tavern turn showing the mature cycle before the final fights.
- **dogdog 7:38** — commits to the Elemental branch.
- **dogdog 11:26** — searches for additional Nomi copies while the shop engine develops.
- **dogdog 14:44** — evaluates whether Golden Brann makes the cycle self-sustaining.
- **dogdog 15:14** — discusses when Nomi should leave and how to convert Tavern stats.
- **dogdog 17:07** — identifies Golden Brann as the demonstrated economy ceiling.
- **dogdog 18:35** — says Nomi must be sold soon as the board converts.
- **Jeef 5:29** — Nomi, Air Revenant and Brann define the shop-scaling direction.
- **Jeef 7:44** — Captain Sanders creates Golden Nomi; treat this as hero acceleration rather than the ordinary gate.
- **Jeef 13:03** — Tavern Tempest triples while the cycle and Unbound conversion develop.
- **Jeef 15:25** — Kelp Keeper extends the Battlecry cycle before the winning finish.
