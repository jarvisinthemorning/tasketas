---
title: Pirates APM Golden
slug: pirates-apm-golden
season: 14
modes:
- solo
tribes:
- pirate
tags:
- season 14
- APM
- golden minions
- discovers
- bounties
classification: meta
core:
- 132762
- 122516
- 132925
addons:
- 122520
- 96786
- 132921
- 132987
- 104448
- 133712
- 132764
- 99035
cycle:
- 132762
- 122516
- 122520
- 96786
- 132921
packages:
- title: Commit
  purpose: Escapee opens the route only when your economy can repeatedly spend Gold and accelerate its Lockbox.
  badge: Commit signal — Escapee + Gold
  optional: false
  cards: [132762]
- title: Core
  purpose: Escapee supplies delayed Goldens, Rogers converts spending into Bounties, and actual Discovers fire Hooktusk's scaling for your other Pirates.
  badge: Required core
  optional: false
  cards: [132762, 122516, 132925]
- title: Bounty engine
  purpose: Rogers generates Bounties while Privateer doubles each cast; keep spending only while the rewards fund useful actions.
  badge: Optional — APM fuel
  optional: true
  cards: [122516, 122520]
- title: Discover fuel
  purpose: Castaway supplies an exact Discover trigger for Hooktusk; random Bounties and Lockbox rewards do not.
  badge: Optional — Hooktusk triggers
  optional: true
  cards: [132921]
- title: Source Golden Touch highroll
  purpose: Parrot can earn Golden Touch; the source's Sphere copies the last Tavern spell twice, which is exceptional acceleration rather than baseline Pirates.
  badge: Optional — source highroll
  optional: true
  cards: [132987, 104448, 133712]
- title: Battlecry bridge
  purpose: Keep Brann while doubled resource Battlecries justify the slot, then sell him when the permanent Pirate engine needs the board space.
  badge: Optional — economy bridge
  optional: true
  cards: [96786]
- title: Dagger Admiration conversion
  purpose: Dagger can copy an Admiration Brann each turn; an all-type Brann beside Poet can then retain the copied combat stats.
  badge: 'Optional — source highroll: trinket + Dark Gift'
  optional: true
  cards: [133713, 132207, 96786, 108463]
- title: Scaling and carries
  purpose: Let Hooktusk scale Pirates through Discovers, bank Golden-play growth on Extortionist, and keep Blade Collector scaled so its attacks threaten adjacent enemies.
  badge: Optional — combat conversion
  optional: true
  cards: [132925, 132764, 99035]
related_routes: []
composition_minions:
- {card_id: 132762, count: 1, golden_count: 0}
- {card_id: 122516, count: 1, golden_count: 0}
- {card_id: 132925, count: 1, golden_count: 0}
composition_spells: []
board_examples:
- stage: mid
  turn: 10
  timestamp: 510
  phase: tavern
  image: /static/boards/pirates-apm-golden-mid.webp
  note: A stable recruit turn where the Golden and Discover engines are online, but economy pieces still compete with the permanent Pirate board for space.
- stage: late
  turn: 14
  timestamp: 1095
  phase: tavern
  image: /static/boards/pirates-apm-golden-late.webp
  note: A stable late Tavern state showing why the APM shell must eventually give way to scaled combat bodies and a finished board.
- stage: late
  turn: 15
  timestamp: 2040
  phase: tavern
  image: /static/boards/pirates-apm-golden-escapee-engine.webp
  note: A second source's clean Recruit turn after the Escapee engine matures, useful for judging which economy slots must become combat cards.
discovery_sources:
- type: hsreplay
  url: https://hsreplay.net/battlegrounds/comps/89/pirates-apm-golden
  comp_id: '89'
- type: firestone
  url: https://www.firestoneapp.com/battlegrounds/comps
  comp_id: pirate_discover
supporting_sources:
- type: youtube
  url: https://www.youtube.com/watch?v=ti8h4WQoG2Q
  author: Rdu Hearthstone
  label: Escapee, Rogers and Privateer execution with board-space cuts
  timestamp: 1535
- type: youtube
  url: https://www.youtube.com/watch?v=FvZJNm95cps
  author: Rdu Hearthstone
  label: Triple-Escapee ceiling and Hooktusk timing
  timestamp: 555
- type: youtube
  url: https://www.youtube.com/watch?v=zITEQk66_0E
  author: BeterBabbit
  label: Lockbox transition with Golden Brann acceleration
  timestamp: 0
- type: youtube
  url: https://www.youtube.com/watch?v=DqPYeFZch0c
  author: Shadybunny
  label: Maldraxxus Dagger and Admiration Brann conversion with Persistent Poet
  timestamp: 850
source:
  type: youtube
  url: https://www.youtube.com/watch?v=IvdTja9QGqg
  author: Shadybunny2
video:
  id: IvdTja9QGqg
  timestamp: 293
source_published_at: '2026-08-08'
verified_at: '2026-08-20'
---

## How it works

[[card:132762|Enterprising Escapee]] is the early route signal. Every 5 Gold spent either creates a [[card:132766|Lockbox]] or shortens the one already in hand; when it opens, it gives a random Golden typed minion. Playing that Golden improves the future scaling granted by [[card:132925|Hooktusk, Master Marauder]], but the Lockbox does not Discover and does not trigger Hooktusk by itself.

[[card:122516|Sky Admiral Rogers]] converts every 9 Gold spent into a random Bounty. [[card:122520|Proud Privateer]] makes each Bounty cast twice, so the useful outcomes can add stats, cards, or Gold while the turn continues. Bounties still do not inherently Discover. Hooktusk needs an exact Discover effect such as [[card:132921|Clever Castaway]], a [[card:59604|Triple Reward]], or the source's Dark Gifts. The repeatable APM cycle is therefore: spend Gold, resolve random resources, play useful Golden minions, fire actual Discovers, and feed Hooktusk. It is not literally infinite; Bounty RNG, Tavern offers, board and hand space, available Gold, and the timer all cap it.

[[card:96786|Brann Bronzebeard]] is a bridge, not the composition's Gold engine. He doubles useful Battlecries while the build is assembling, but he does not double Rogers, Escapee, Hooktusk, or Bounty casts. The source eventually sells Brann to make room for Rogers and permanent combat pieces.

Shadybunny2's game receives unusually strong acceleration from Nightmare Lord Xavius's Dark Gifts. [[card:132987|Treasure Parrot]] earns [[card:104448|Golden Touch]] after dealing enough damage, then [[card:133712|Sphere of Memory]] copies the last Tavern spell twice at the end of the turn. Keeping Golden Touch last explains the video's repeated free copies; Parrot alone is not an every-turn generator. The current HSReplay Core—Escapee, Rogers, and Hooktusk—is the baseline route, not evidence that an ordinary lobby receives the source's Golden supply or final numbers.

## When to commit

- **Real signal:** Escapee plus enough current and future Gold to trigger it repeatedly. One Escapee on ordinary income creates a slow Lockbox, not an APM composition.
- **Core online:** add Rogers when repeated spending can produce several Bounties, then add Hooktusk only when played Goldens can improve its buff and exact Discover effects can trigger it.
- **Good acceleration:** Treasure Parrot can turn combat damage into Golden Touch, while Brann can multiply Battlecry resources during the transition.
- **Not enough:** Rogers without sustained spending, Hooktusk without Discovers, or Golden minions without a payoff. Each is a component; none creates the full loop alone.
- **Abort condition:** if the Lockbox is too slow, Bounties do not refund useful resources, or the timer is already winning the APM race, preserve the strongest Pirates and stop paying for future turns.

## Shopping and sequencing

1. Buy Escapee only when you can immediately spend toward its first Lockbox and have a realistic way to shorten the timer again. Keep lower-tier Gold and card generators only while they produce more actions than they consume.
2. Add Rogers when 9-Gold cycles will occur repeatedly. Track its counter before refreshing so the last spend produces a Bounty instead of an empty shop and no time to use it.
3. Add Proud Privateer when doubled Bounties are worth a Tier 5 board slot. Privateer does not create Bounties by itself; it multiplies the ones Rogers or another generator already supplies.
4. Add exact Discover fuel such as Clever Castaway. Lockboxes and random Bounties are resources, not Hooktusk triggers.
5. Play useful Golden minions before long Discover chains so Hooktusk's future buffs are improved first. Then resolve Discovers while the Pirates that should receive the scaling are already on board.
6. Use Brann to double concrete Battlecry resources, not as a reason to buy every Battlecry. The source removes him once Rogers and the permanent Pirate shell need the space.
7. Keep [[card:132764|Maritime Extortionist]] when enough Golden minions have already been played to make it a real body. Its growth is retrospective, so it can be bought late without sitting on board through the whole setup.
8. Add [[card:99035|Blade Collector]] early enough for Hooktusk and Bounty stats to land on it. Its own attacks hit adjacent enemies, so the effect matters only when Blade Collector is large enough to survive and reach a useful target.
9. Stop cycling before the rope. Play the final Golden minions, finish Discovers, sell temporary economy, field seven combat cards, and check order rather than entering combat with half the engine in hand.

## Escapee execution checkpoints

- **Do not level away the Lockbox turn.** The supporting source runs out of Gold after leveling before Rogers is online. Stay when another Escapee trigger, Golden cash-out, or stable combat matters more than one Tavern Tier.
- **Sequence Golden cash-outs before Discover scaling.** When a Lockbox is about to open, leave hand and board space, play the useful Golden first, then resolve Hooktusk Discovers.
- **Rogers and Privateer are working slots, not sacred furniture.** Keep them while doubled Bounties fund the turn. Once the engine sustains itself without that package, replace Rogers with cleave or another finished combat body and preserve one cycle slot.
- **Buy time as carefully as Gold.** Rdu calls the route difficult even with the pieces assembled. Decide likely cuts before the APM turn starts; improvising seven board slots under the rope is how the Tavern becomes an escape room.

## Dagger Admiration conversion

The Shadybunny commentary game adds a premium late conversion after the ordinary Escapee/Hooktusk engine is already working. [[card:133713|Maldraxxus Dagger]] repeatedly copies a gifted [[card:96786|Brann Bronzebeard]] carrying [[card:132207|Admiration]]. Once Brann has all minion types, placing it beside [[card:108463|Persistent Poet]] preserves the combat-start stats that would otherwise disappear.

This is a teachable finish, not better baseline progression. It requires the specific trinket, Dark Gift, and all-type setup; it does not replace Escapee as the Gold generator or Hooktusk as the permanent Pirate payoff. If those premium pieces do not arrive, sell Brann when his Battlecry economy stops paying for the slot and finish the normal Pirate board.

## Positioning and traps

- **Golden first, Discover second:** Hooktusk's scaling is improved by Golden minions already played this game. Reversing the order leaves permanent stats behind.
- **Random is not Discover:** Lockboxes, Golden Touches, and Bounties can supply resources, but none fires Hooktusk unless the effect explicitly says Discover.
- **Do not credit Brann for passive triggers:** he doubles Battlecries only. Proud Privateer doubles Bounties; neither card substitutes for the other.
- **Leave working space:** Lockboxes, Golden minions, Triple Rewards, Discovers, and Bounties all compete for hand and board slots. Sell low-impact economy before the turn becomes seven cards of administrative debt.
- **Protect the cleave:** Blade Collector needs enough stats and a clean attack. Check Taunt placement and avoid exposing it to an obvious opposing cleave or early removal when another attacker can go first.
- **Keep the payoff bodies present:** Hooktusk buffs other Pirates, so selling the intended recipients during the Discover chain wastes the scale.
- **Do not chase the source ceiling:** Dark Gifts and repeated Golden Touches supplied exceptional Golden density. A normal game should convert earlier and accept a smaller but complete combat board.
- **Mobile warning:** the newer source explicitly calls the route poor on mobile. If animations or input make full APM turns unrealistic, convert the first strong Golden/Hooktusk cycle into combat instead of hoarding a theoretical infinite turn.

## After a loss

- **Escapee never paid off:** you committed without enough Gold to advance the Lockbox or too late for its delayed Golden reward.
- **Rogers felt empty:** you did not spend enough to trigger several Bounties, or you generated them after the timer and board space could no longer use the rewards.
- **Hooktusk barely scaled:** you found it before establishing Golden plays, or mistook random Lockbox and Bounty rewards for Discover triggers.
- **Played Goldens but saw no stats:** Golden plays improve Hooktusk's next Discover-triggered buff; they do not fire the buff themselves.
- **The turn ended with resources stranded:** you kept Brann or other temporary economy too long, then ran out of hand space, board space, or time.
- **Huge stats still lost:** the final board lacked cleave protection, attack order, or enough combat utility after the economy shell was removed.
- **The source looked much stronger:** its Dark Gifts, Treasure Parrots, and Sphere of Memory copies were acceleration, not evidence that the baseline Core always reaches that ceiling.

## Useful timestamps

- **4:53** — The source commits to Pirates after receiving strong Golden and combat acceleration.
- **6:50** — Hooktusk and Brann are evaluated as the route begins to form.
- **8:08** — The plan becomes explicit: play Golden minions, create more value, and continue spending.
- **12:52** — The source recognizes that one Hooktusk is limiting the permanent scaling.
- **15:00** — Brann is sold so Rogers and the permanent Pirate board can take over.
- **18:15** — The final recruit turn starts with the mature engine visible and enough time to convert.
- **20:06** — The game ends in a win despite a final positioning mistake, reinforcing that APM still needs a combat check.
- **Rdu 0:38** — the Escapee, Rogers and Privateer engine is stated before the game develops.
- **Rdu 11:42** — missing Rogers causes the first run-out; leveling timing is questioned.
- **Rdu 14:04** — the source calls the composition hard and weighs Escapee against cleave.
- **Rdu 25:22** — Lockbox is identified as the pivot and its acceleration is explained.
- **Rdu 32:55** — the mature engine evaluates whether Castaway and the Bounty package are still needed.
- **Rdu 35:51** — Rogers becomes the cut for cleave, leaving one cycle slot.
- **Rdu 43:43** — explicit warning that the APM route is not mobile-friendly.
- **Shadybunny commentary 6:40** — the Pirate engine is established; the title's Brann payoff is not yet the primary route.
- **Shadybunny commentary 14:10** — Dagger, Admiration Brann, and Poet conversion are visible on a stable Recruit board.
- **Shadybunny commentary 19:40** — stable mature Tavern board with the Gift-gated conversion online.
