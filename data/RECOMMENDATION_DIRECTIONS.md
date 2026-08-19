# Recommendation Direction Architecture v1

Titles: **81**
Authored directions: **330**

## Principle

Relatedness and recommendation direction are separate layers. Route labels describe the computed move from source to target and remain review aids.

## Primary route distribution

- **safe-next-step**: 29
- **adjacent-style**: 39
- **higher-intensity**: 101
- **lower-friction**: 63
- **more-emotional**: 49
- **more-belt-forward**: 7
- **more-movement-driven**: 8
- **more-narrative-driven**: 9
- **hookier**: 3
- **wild-card-bridge**: 6
- **catalog-authored**: 16

## High-confidence examples

- `greatest -> hairspray` | **safe-next-step** | distance 0.389
- `hairspray -> greatest` | **safe-next-step** | distance 0.389
- `batboy -> repo` | **safe-next-step** | distance 0.409
- `moana -> encanto` | **safe-next-step** | distance 0.41
- `encanto -> moana` | **safe-next-step** | distance 0.41
- `moana -> annie` | **safe-next-step** | distance 0.436
- `annie -> moana` | **safe-next-step** | distance 0.436
- `once -> lalaland` | **safe-next-step** | distance 0.445
- `lalaland -> once` | **safe-next-step** | distance 0.445
- `waitress -> tickstage` | **safe-next-step** | distance 0.448
- `tickstage -> waitress` | **safe-next-step** | distance 0.448
- `blinded -> walkline` | **safe-next-step** | distance 0.455
- `hairspray -> legallyblonde` | **safe-next-step** | distance 0.469
- `legallyblonde -> hairspray` | **safe-next-step** | distance 0.469
- `once -> beginagain` | **safe-next-step** | distance 0.472
- `beginagain -> once` | **safe-next-step** | distance 0.472
- `greatest -> kpop` | **safe-next-step** | distance 0.473
- `kpop -> greatest` | **safe-next-step** | distance 0.473
- `hamilton -> ticktick` | **safe-next-step** | distance 0.499
- `ticktick -> hamilton` | **safe-next-step** | distance 0.499
- `hedwig -> hedwigstage` | **safe-next-step** | distance 0.514
- `hedwigstage -> hedwig` | **safe-next-step** | distance 0.514
- `hedwigstage -> rent` | **safe-next-step** | distance 0.549
- `rent -> jcs` | **safe-next-step** | distance 0.553
- `jcs -> rent` | **safe-next-step** | distance 0.553
- `spirited -> prom` | **safe-next-step** | distance 0.583
- `prom -> spirited` | **safe-next-step** | distance 0.583
- `mammamia -> pitchperfect` | **safe-next-step** | distance 0.596
- `pitchperfect -> mammamia` | **safe-next-step** | distance 0.596

## Low-confidence review queue

- `wicked -> phantom` | catalog-authored | distance 0.622
- `rockyhorrorlive -> priscilla` | catalog-authored | distance 0.667
- `singstreet -> once` | catalog-authored | distance 0.708
- `singstreet -> beginagain` | catalog-authored | distance 0.747
- `walkline -> beginagain` | catalog-authored | distance 0.801
- `yesterday -> beginagain` | catalog-authored | distance 0.848
- `hamilton -> inside` | catalog-authored | distance 0.91
- `blinded -> beginagain` | catalog-authored | distance 0.999
- `moulin -> odessa` | catalog-authored | distance 1.088
- `waitress -> lastfive` | catalog-authored | distance 1.098
- `kpop -> jamie` | catalog-authored | distance 1.221
- `moulin -> mammamia` | catalog-authored | distance 1.247
- `wicked -> colorpurple` | catalog-authored | distance 1.275
- `across -> walkline` | catalog-authored | distance 1.329
- `hamilton -> heights` | wild-card-bridge | distance 1.359
- `rocketman -> walkline` | catalog-authored | distance 1.42
- `comefromaway -> once` | wild-card-bridge | distance 1.5
- `rocketman -> bohemian` | catalog-authored | distance 1.506
- `waitress -> once` | wild-card-bridge | distance 1.539
- `across -> yesterday` | wild-card-bridge | distance 1.606
- `legallyblonde -> meangirls` | wild-card-bridge | distance 1.718
- `westside -> lalaland` | wild-card-bridge | distance 1.857
