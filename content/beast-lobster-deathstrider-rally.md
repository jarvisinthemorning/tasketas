---
title: Lobster Deathstrider Rally
slug: beast-lobster-deathstrider-rally
season: 14
modes:
- solo
tribes:
- beast
tags:
- season 14
- deathrattle
- rally
- scaling
classification: meta
core:
- 132796
- 132808
addons:
- 108909
- 97408
- 132802
- 132804
- 133400
- 67213
cycle: []
packages:
- title: Commit
  purpose: Commit only when Lobster is already improved and you have a premium trigger engine—preferably Golden Deathstrider, or Deathstrider plus Titus and multiple Rally attacks.
  badge: Commit signal — premium engine + trigger density
  optional: false
  cards: [132796, 132808, 132806, 132800]
- title: Core
  purpose: Use Rally attacks to trigger Lobster repeatedly in combat; use Fishbaits for permanent Tavern-phase stats.
  badge: Required core
  optional: false
  cards: [132796, 132808]
- title: Rally
  purpose: Any Rally attacker triggers Deathstrider. Prefer useful early bodies and Windfury for extra triggers.
  optional: true
  cards: [132806, 132800, 95286, 70173, 70157, 126637]
- title: Fishbait
  purpose: Create Fishbaits with Lionfish or Snarky Shark, then feed them to your left-most Beast.
  optional: true
  cards: [132802, 132794, 132804]
- title: Add-ons
  purpose: Reborn gives Lobster another Deathrattle; Titus doubles every Lobster Deathrattle trigger.
  optional: true
  cards: [108909, 97408]
- title: Wolfhead Flail ceiling
  purpose: Flail plus Titus and Drakkari can turn a wide Lobster board into an end-of-turn engine, replacing rather than merely boosting Deathstrider Rally.
  badge: Optional — trinket highroll
  optional: true
  cards: [133400, 97408, 101314, 132796]
- title: Fish of N'Zoth copying
  purpose: A Dark Gift can supply Fish copies that retain Lobster Deathrattles in combat; neither Fish access nor multiple copies is an ordinary Tavern expectation.
  badge: Optional — Dark Gift highroll
  optional: true
  cards: [67213, 132796, 97408]
- title: Herald Sticker duplication
  purpose: Herald Sticker fires every friendly Deathrattle before combat; Souvenir Stand can copy it for a second premium activation.
  badge: Optional — trinket ceiling
  optional: true
  cards: [120926, 112895, 132796, 97408]
- title: Treasure Parrot conversion
  purpose: A Parrot that earns Golden Touch can convert a strong Tavern roll into a Golden Titus or Deathstrider, but cannot be your baseline plan.
  badge: Optional — generated Golden ceiling
  optional: true
  cards: [132987, 104448, 97408, 132808]
board_examples:
- stage: early
  turn: 7
  timestamp: 90
  phase: tavern
  image: /static/boards/beast-lobster-deathstrider-rally-early.webp
  note: A clean recruit snapshot before the source's later setup, useful as a transition baseline.
- stage: mid
  turn: 8
  timestamp: 120
  phase: tavern
  image: /static/boards/beast-lobster-deathstrider-rally-mid.webp
  note: The intermediate recruit state shows the developing line rather than skipping directly to the final board.
- stage: late
  turn: 9
  timestamp: 149
  phase: tavern
  image: /static/boards/beast-lobster-deathstrider-rally-late.webp
  note: The last clean Tavern snapshot before this edited source moves into combat-heavy footage.
- stage: late
  turn: 11
  timestamp: 709
  phase: tavern
  image: /static/boards/beast-lobster-deathstrider-premium.webp
  note: A clean Recruit-phase view of a premium Lobster engine after Titus/Flail support is established, not a baseline final board.
composition_minions:
- {card_id: 132796, count: 1, golden_count: 0}
- {card_id: 132808, count: 1, golden_count: 0}
- {card_id: 132800, count: 1, golden_count: 0}
composition_spells: []
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/87/beasts-tasty-lobstah
  comp_id: '87'
- type: firestone
  url: https://www.firestoneapp.com/battlegrounds/comps
  comp_id: beast_lobster
supporting_sources:
- type: youtube
  url: https://www.youtube.com/watch?v=Bf9VfxtDWQI
  author: Rdu Hearthstone
  label: Stricter Golden Deathstrider commit gate
  timestamp: 0
- type: youtube
  url: https://www.youtube.com/watch?v=SapUxehxlu8
  author: dogdog
  label: Titus and Wolfhead Flail premium ceiling
  timestamp: 709
- type: youtube
  url: https://www.youtube.com/watch?v=caFAHGy_ebE
  author: dogdog
  label: Dark Gift-created Fish of N'Zoth package
  timestamp: 560
- type: youtube
  url: https://www.youtube.com/watch?v=j3rg2SW84Us
  author: Shadybunny
  label: Double Herald Sticker and Treasure Parrot Golden Touch ceiling
  timestamp: 594
- type: youtube
  url: https://www.youtube.com/watch?v=FJyKGdqRj4Q
  author: Shadybunny
  label: Wolfhead Flail end-of-turn Lobster conversion
  timestamp: 706
- type: youtube
  url: https://www.youtube.com/watch?v=KyFz2BZj27w
  author: Shadybunny
  label: Golden Windfury Gryphon into stacked Deathstrider Rally ceiling
  timestamp: 340
source:
  type: youtube
  url: https://www.youtube.com/watch?v=rJ66OM7pENQ
  author: HIQ MU
video:
  id: rJ66OM7pENQ
  timestamp: 180
source_published_at: '2026-08-07'
verified_at: '2026-08-18'
---

## How it works

Keep [[card:132796|Tasty Lobster]] as your left-most Deathrattle. Every friendly Rally minion that attacks lets [[card:132808|Deathstrider]] trigger it again. Windfury Rally minions can trigger it twice.

[[card:132794|Lurking Lionfish]] and [[card:132804|Snarky Shark]] create [[card:132802|Fishbait]] in the Tavern. Your left-most Beast attacks it and keeps the +5/+5 permanently. Headhunter Gryphon is source-demonstrated; the other Rally cards above are current-pool, mechanically compatible shopping options.

## Pivot signal

- **Hold Lobster for tempo; do not force the comp from Lobster alone.**
- **Commit:** an already improved Lobster plus a premium trigger engine—preferably Golden Deathstrider, or plain Deathstrider with Titus and multiple Rally attacks that can actually connect.
- **Abort:** if Deathstrider is plain, Titus is absent, or the Rally bodies cannot reliably attack, keep Lobster as tempo and stay ready to leave the route.
- **Best upgrades:** Windfury Rally attackers, [[card:97408|Titus Rivendare]], and more Lobsters after the hidden improvement has grown.

## Premium ceilings

- **Wolfhead Flail:** [[card:133400|Wolfhead Flail]] triggers all friendly Deathrattles at end of turn. With [[card:97408|Titus Rivendare]], [[card:101314|Drakkari Enchanter]], and several Lobsters, it can become a separate end-of-turn conversion that no longer needs Deathstrider or Rally. This is a trinket-and-golden ceiling, not ordinary Core; the source explicitly calls it an end-of-turn comp despite the video's Deathrattle marketing.
- **Fish copies:** a source-specific Dark Gift discovers a plain copy of a gifted warband minion, allowing additional [[card:67213|Fish of N'Zoth]]. Fish can retain Lobster Deathrattles during combat, but the copied access and multiple Fish are Gift-gated.
- **Herald duplication:** [[card:120926|Herald Sticker]] triggers every friendly Deathrattle at the start of combat. [[card:112895|Souvenir Stand]] can become a second Sticker, but this double activation is a trinket highroll rather than ordinary progression.
- **Golden conversion:** [[card:132987|Treasure Parrot]] can earn [[card:104448|Golden Touch]] after dealing enough damage. The supporting source uses that reward to create premium Golden trigger pieces; buy Parrot only when it can realistically connect, not as a substitute for the Core.
- **Golden ceiling:** Golden Deathstrider, repeated Titus triggers, Flail, and several Fish copies are source ceilings—not a seven-card shopping checklist. The ordinary line should convert sooner and accept fewer triggers.

## Positioning and traps

- Lobster must be your **left-most Deathrattle** for Deathstrider.
- Rally minions must survive long enough to attack; Windfury only helps if both attacks happen.
- Lionfish and Snarky Shark make your **left-most Beast** attack Fishbait, so move the Beast you want to keep scaling into that slot first.
- Titus doubles the Deathrattle, but it does not replace Rally trigger density.
- Rally support without Deathstrider does nothing for the Lobster plan; the Fish source explicitly delays buying it until Titus and the missing payoff are found.
- Do not sacrifice the whole board to preserve a premium fantasy. The supporting sources repeatedly run into too many necessary pieces and late board-space choices.

## Useful timestamps

- **dogdog 4:12** — questions an unsupported Lobster and describes its ordinary cap as low.
- **dogdog 5:09** — Titus appears; this is the point where the source actually commits.
- **dogdog 11:48** — identifies Drakkari and more Titus copies as the remaining upgrades while Flail is already owned.
- **dogdog 13:23** — describes the Golden Deathstrider/Golden Titus ceiling.
- **Fish source 9:20** — Dark Gift discovers a plain gifted warband copy and selects Fish.
- **Fish source 11:21** — Rally support is rejected before Titus and Deathstrider; the source calls out the number of required pieces.
- **Fish source 16:23** — board space forces a choice between another large Lobster and another Fish.
- **Herald source 9:54** — Souvenir Stand duplicates Herald Sticker, creating two start-of-combat Deathrattle activations.
- **Herald source 13:42** — Treasure Parrot is evaluated as access to Golden Touch; Deathstrider is found moments later.
- **Herald source 17:29** — Golden Touch creates Golden Titus and the premium engine finally comes online.
- **Herald source 22:48** — stable late Tavern board shows the mature double-Sticker/Golden-trigger ceiling.
- **Flail source 11:46** — Wolfhead Flail makes the end-of-turn commitment explicit after the source rejects an unsupported Deathstrider line.
- **Flail source 18:46** — five Lobsters with Golden Drakkari and Golden Titus produce the first mature end-of-turn board.
- **Flail source 23:52** — the premium Goldenizer ceiling reaches 63 end-of-turn Lobster triggers; this is not a normal Rally expectation.
- **Gryphon source 5:40** — Lobster joins Golden Windfury Gryphon and Golden Titus, creating the soft commit.
- **Gryphon source 7:10** — Deathstrider completes the actual Rally trigger engine.
- **Gryphon source 14:57** — two Golden Deathstriders plus another copy show the generated-Golden APM ceiling, not a baseline board.
