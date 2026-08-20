---
title: Bristlemane–Juggernaut Gem Transfer
slug: quilboar-bristlemane-juggernaut
season: 14
patch: '36.2.0'
modes: [solo]
tribes: [quilboar]
tags: [season 14, blood gems, spell targeting, rally, stat transfer]
classification: variant
core: [132320, 132636]
addons: [116434, 130298]
cycle: []
flex: [126671, 96786]
packages:
  - title: Commit
    purpose: Improve Blood Gems while keeping both Quilboar payoff routes open until the shop gives you a real engine.
    badge: Commit signal
    optional: false
    cards: [116434]
  - title: Core
    purpose: Jailbird Juggernaut is the shared Rally payoff that turns concentrated Blood Gems into recurring Golems.
    badge: Required core
    optional: false
    cards: [132636]
  - title: Bristlemane loading
    purpose: Target Vigilant Bristlemane with spells so Juggernaut keeps receiving permanent Gems before Rally.
    badge: Choose one loader
    optional: false
    cards: [132320, 132636]
  - title: Confiscation loading
    purpose: Let Vineweaver or other neighbors build Gems, then consolidate them onto Juggernaut with repeatable Gem Confiscation.
    badge: Choose one loader
    optional: false
    cards: [126671, 122562, 110642, 132636]
  - title: Blood Gem generators
    purpose: Feed targeted casts, immediate tempo, and the Gem package that your chosen Golem core converts.
    badge: Shopping support
    optional: true
    cards: [70143, 70157, 116182, 122098, 132630, 126669, 126667, 70173, 132929]
  - title: Late upgrades
    purpose: Duplicate targeted spells or permanently raise every Blood Gem once the Golem engine is already online.
    badge: Optional — luxury ceiling
    optional: true
    cards: [130298, 122566, 80755]
  - title: Aggem Sticker ceiling
    purpose: Sticker can flood a menagerie board with end-of-turn Gems, but it accelerates the existing loader rather than replacing Bristlemane or Confiscation.
    badge: Optional — trinket highroll
    optional: true
    cards: [121132, 132320, 132636]
related_routes:
  - title: Gem Rat → Turbo Hogrider
    slug: quilboar-choose-one-hogrider
    purpose: Switch when Turbo Hogrider and repeatable Choose One cards arrive before a credible Golem loader.
    cards: [116195, 116190, 132632]
board_examples:
  - stage: late
    timestamp: 1300
    phase: tavern
    image: /static/boards/quilboar-bristlemane-juggernaut-late.webp
    note: Use this mature Tavern state as the visual payoff benchmark; earlier candidates were obstructed or combat.
discovery_sources:
  - type: hsreplay
    url: https://hsreplay.net/battlegrounds/comps/90/quilboar-bristlemane
    comp_id: '90'
supporting_sources:
  - type: youtube
    url: https://www.youtube.com/watch?v=j3DY6PNRCcA
    author: dogdog
    label: Aggem Sticker loader and anti-Beast first-place demonstration
    timestamp: 900
composition_minions:
- {card_id: 126671, count: 1, golden_count: 0}
- {card_id: 132320, count: 1, golden_count: 0}
- {card_id: 132636, count: 1, golden_count: 0}
composition_spells:
- {card_id: 110642, count: 1}
source:
  type: youtube
  url: https://www.youtube.com/watch?v=08tFc8FYcsI
  author: Shadybunny
video:
  id: 08tFc8FYcsI
  timestamp: 309
source_published_at: '2026-08-01'
verified_at: '2026-08-18'
---

## Game plan

Use [[card:132320|Vigilant Bristlemane]] to turn targeted spells into repeated Blood Gems on its adjacent minions. The demonstrated line first grows a pool of Gem stats, then concentrates them onto [[card:132636|Jailbird Juggernaut]]. Juggernaut converts that permanent investment into Rally pressure by repeatedly summoning and immediately attacking with a Blood Golem based on the transferred Gem stats.

This is deliberately separate from the Choose One Turbo Hogrider guide. Hogrider rewards Choose One volume across the board; this line rewards repeatedly targeting Bristlemane and eventually moving the accumulated Gems onto one Rally carry.

## When to commit

Gem Rat is the soft commitment signal: it improves Blood Gems while leaving both Hogrider and Golem payoffs open. Do not hard-lock this page because you found one Bristlemane. For the Golem route you still need three things:

- enough cheap targeted spells or Blood-Gem generation to trigger Bristlemane repeatedly;
- two adjacent minions worth receiving the Gems during the scaling phase; and
- a credible way to move the accumulated Gems onto Juggernaut before the lobby outruns you.

A Golden Bristlemane is a major acceleration point because each targeted cast applies twice as many Gems to both neighbors. [[card:116434|Gem Rat]] is the shared starting signal, not the payoff; switch to the linked Hogrider route if its actual core arrives first.

## How to play

1. **Scale through Bristlemane.** Keep it between two permanent or at least sell-safe bodies while casting targeted spells on it. Each cast should improve both adjacent minions rather than strand Gems on a disposable slot.
2. **Preserve transfer access.** Do not spend every Gem-transfer effect early. The source builds broadly, then moves the large Gem package onto Juggernaut once the Rally carry is ready.
3. **Add Juggernaut before the final transfer.** A small Juggernaut is not a win condition. Its Blood Golem inherits the Blood-Gem contribution, so the card becomes threatening only after the concentrated transfer.
4. **Use [[card:130298|Balinda Stonehearth]] as an accelerator, not a requirement.** Targeted friendly spells cast twice, which can multiply Bristlemane triggers, but the source treats the late Golden Balinda as luxury rather than the reason to enter the comp.
5. **Open board space before combat.** Rally needs room to summon. The source explicitly notes that repeated Juggernaut triggers can be throttled by a crowded board.
6. **Keep trinket acceleration in its lane.** [[card:121132|Aggem Sticker]] can provide a huge end-of-turn Gem supply across minion types, but the supporting source still needs Bristlemane/Confiscation loading and Juggernaut conversion. Sticker is ceiling, not Core.

## Positioning

Keep Bristlemane between the two units you actually want to scale during Recruit. Once Juggernaut becomes the carry, move it early enough in attack order to start producing Blood Golems before support pieces die or summon space disappears.

Juggernaut is particularly awkward for a taunted Leeroy plan: the summoned Golem attacks immediately, so it can consume the Leeroy hit before the main carry is exposed.

## Failure modes

- **No transfer:** large Gems on temporary bodies do not help Juggernaut if you cannot move them.
- **Tiny Gem package:** assembling the named cards without meaningful Blood-Gem stats produces small Golems and loses to ordinary scaling.
- **No summon space:** a full board can waste the Rally ceiling even when Juggernaut is enormous.
- **Greedy luxury pieces:** the source's Golden Balinda is spectacular but optional. Do not delay the core transfer while fishing for it.
- **Overlapping the wrong shell:** if your real engine is repeated Choose One cards plus Turbo Hogrider, follow that line instead of forcing Bristlemane into it.
- **Mistaking a trinket for the route:** Aggem Sticker makes the source spectacular, but the ordinary decision is still whether you can load and transfer enough Gems into Jailbird.

## Demonstrated ceiling

At **21:40**, the stable Tavern board shows Golden Jailbird Juggernaut at **8.2k/8.8k**, backed by Golden Gem Rat and Golden Balinda. The following combat visibly demonstrates the enormous Blood Golems produced by the Rally chain. The available source does not show an explicit victory/result screen, so this is evidence of the comp's endgame conversion—not a claimed first-place result.

## Useful timestamps

- **5:09** — Shady identifies Vigilant Bristlemane and explains why the Golden scaling trigger matters.
- **5:42** — The targeted-spell interaction is broken down: the cast turns into Blood Gems on both adjacent minions.
- **8:11** — Jailbird Juggernaut is identified as the best final buff target because Rally summons a Golem from its Blood-Gem stats.
- **10:18** — The source starts concentrating buffs onto Juggernaut and discusses moving it earlier in attack order.
- **15:01** — Commentary explains the repeated Rally ceiling and the board-space constraint.
- **16:49** — The large Gem package is transferred onto the intended carry.
- **20:11** — Golden Juggernaut is visibly above 3k while the final package is still being assembled.
- **21:40** — Stable final Tavern board: 8.2k/8.8k Golden Juggernaut.
- **23:00** — The enormous Blood Golems produced by the Juggernaut Rally chain are visible in combat.
- **Supporting source 6:34** — the player commits to Gems before selecting Aggem Sticker; the trinket is acceleration, not the route's identity.
- **Supporting source 11:43** — Turbo Hogrider is offered and rejected, confirming that this remains the Bristlemane–Juggernaut route.
- **Supporting source 15:00** — the exact plan is stated: load Vigilant Bristlemane, then move the Gems onto Jailbird Juggernaut.
- **Supporting source 22:54** — the final combat confirms the Rally carry and anti-Beast tech win the lobby.

The linked commentary is based on JeefHS's original gameplay upload:
<https://www.youtube.com/watch?v=FZWbxeaiq-w>
