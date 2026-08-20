---
title: Mechs — Magnetics
slug: mechs-magnetics
season: 14
patch: '36.2.2'
modes: [solo]
tribes: [mech]
tags: [magnetic, scaling, end-of-turn]
classification: meta
core: []
addons: []
cycle: []
packages:
  - title: Core
    purpose: Stack Magnetizations with Spark Snapper, double the best stack on Drone Duplicator, then convert every stack into permanent board stats with Utility Drone.
    badge: Required core
    optional: false
    cards: [132676, 132312, 98588]
  - title: Magnetic supply
    purpose: Keep producing Magnetics; Scrap Scraper is the refill engine and Accord-o-Tron is the best Duplicator target when extra Gold still matters.
    badge: Shopping engine
    optional: false
    cards: [98592, 98576]
  - title: End-of-turn multiplier
    purpose: Add Drakkari only after Utility Drone is online so the Magnetization payoff triggers twice.
    badge: Scaling upgrade
    optional: false
    cards: [101314]
  - title: Choice refills
    purpose: Use these optional generators to keep finding useful typed bodies and spells without replacing the Magnetics core.
    badge: Optional — refills
    optional: true
    cards: [133075, 126916]
  - title: Spell-magnetization branch
    purpose: The source's optional branch turns Repair Jobs and Natural Blessings into more Magnetizations, but it needs extra board space and is not the minimum route.
    badge: Optional — source branch
    optional: true
    cards: [132895, 132893, 120905, 130298]
related_routes: []
composition_minions: [132676, 132312, 98588, 98592, 98576, 101314]
composition_spells: []
board_examples:
  - stage: early
    turn: 8
    timestamp: 333
    phase: tavern
    image: /static/boards/mechs-magnetics-early.webp
    note: The Magnetics direction is established, but the board still needs the late end-of-turn converter.
  - stage: end
    turn: 15
    timestamp: 1380
    phase: tavern
    image: /static/boards/mechs-magnetics-end.webp
    note: Last Tavern turn before the visibly verified first-place result.
discovery_sources:
  - type: hsreplay
    url: https://hsreplay.net/battlegrounds/comps/2/mechs-magnetics/
    comp_id: '2'
supporting_sources: []
source:
  type: youtube
  url: https://www.youtube.com/watch?v=vow9zY5FwFg
  author: Sevel
video:
  id: vow9zY5FwFg
  timestamp: 242
source_published_at: '2026-08-16'
verified_at: '2026-08-20'
---

## How it works

[[card:132676|Spark Snapper]] creates a growing Magnetization whenever you play a Mech. Put the stack you most want to preserve on [[card:132312|Drone Duplicator]]: after activating it, the next Magnetization applied to that minion that turn is doubled. [[card:98588|Utility Drone]] is the permanent payoff, turning each friendly minion's accumulated Magnetizations into end-of-turn stats. Once that loop is established, [[card:101314|Drakkari Enchanter]] doubles Utility Drone's end-of-turn trigger.

The directory-linked game uses a broader spell branch as its ceiling. [[card:132895|Rescue Bot]] supplies Repair Jobs, [[card:132893|Glambot]] converts spells cast on Mechs into more Satellites, and [[card:120905|Fauna Whisperer]] plus [[card:130298|Balinda Stonehearth]] add repeated targeted-spell buffs. Treat that package as optional: the creator explicitly debates Fauna versus another Drone and later says Rescue Bot can leave, while the Magnetization-to-Utility-Drone engine remains the route's identity.

## When to commit

- The first real signal is a live [[card:132676|Spark Snapper]] plus repeatable Magnetic generation. The creator names the Snapper setup at **4:02**, and the stable Turn 8 Tavern frame at **5:33** shows the direction surviving into the next recruit turn.
- A Snapper by itself is not enough when the lobby is already pressuring you. Stabilize first, then look for [[card:132312|Drone Duplicator]] and a path to [[card:98588|Utility Drone]].
- [[card:98592|Scrap Scraper]] is the cleanest recurring Tavern-card supply. The current HSReplay package also includes [[card:98576|Accord-o-Tron]], whose start-of-turn Gold makes it the preferred Duplicator stack when economy still matters.

## How to play the recruit turns

1. Buy repeatable Magnetic supply before speculative late support. Every Mech played while Snapper is present adds another Magnetization, so ordinary Mech buys can advance the engine.
2. Activate [[card:132312|Drone Duplicator]] before applying the one Magnetization you most want doubled that turn. Do not spend the activation on a disposable stack if an economy or long-term carry stack is available.
3. Add [[card:98588|Utility Drone]] when several board slots already carry Magnetizations. At **17:06**, the source explicitly chooses Drone over Fauna; by **19:17** the creator says the required setup is present and prefers maximum scaling.
4. Add [[card:101314|Drakkari Enchanter]] only after an end-of-turn payoff is already working. The source calls a Golden Drakkari the missing link after the win, but Golden is a ceiling—not a requirement for the ordinary route.
5. Use [[card:133075|Captain Cookie]] and [[card:126916|Seafloor Recruiter]] as refills when their generated choices improve the board. Do not let optional generation crowd out Snapper, Duplicator, Utility Drone, or the Magnetic stacks they are scaling.

## Positioning and traps

- Keep the durable Magnetic stacks; sell replaceable generators first. The source specifically identifies Rescue Bot as expendable at **20:01**.
- Do not force the source's full mixed Naga/spell board. Nightmare Lord Xavius and the game's trinkets accelerate this particular result, and the video itself repeatedly weighs Fauna, Glambot, Rescue Bot, and an extra Drone against limited board space.
- Utility Drone pays for Magnetization count, not simply large current stats. Buying generic large Mechs without adding Magnetizations misses the comp's permanent scaling engine.
- The verified game finishes **first place**, but that result is evidence that this assembled route produced a mature payoff—not a promise that the same stats or placement are typical.

## Useful timestamps

- **4:02** — Spark Snapper is named as the setup while the creator acknowledges immediate pressure.
- **5:33** — Clean, stable Turn 8 Tavern frame after the Magnetics direction is established.
- **17:06** — Drone is chosen over Fauna.
- **19:17–19:38** — The creator says the setup is complete, chooses maximum scaling, and evaluates the remaining slots.
- **23:00** — Stable final Tavern board before the winning combat.
- **23:50** — Result screen unambiguously shows **1st Place!!!**.
