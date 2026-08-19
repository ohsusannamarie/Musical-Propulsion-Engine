# Recommendation Direction Architecture v2

Titles: **81**
Authored directions: **330**

## Principle

Relatedness and recommendation direction remain separate layers. v2 chooses the primary route by evidence strength rather than classifier rule order.

## Primary route distribution

- **safe-next-step**: 25
- **adjacent-style**: 35
- **higher-intensity**: 18
- **lower-friction**: 19
- **more-emotional**: 37
- **more-belt-forward**: 47
- **more-movement-driven**: 36
- **more-narrative-driven**: 37
- **hookier**: 52
- **wild-card-bridge**: 6
- **catalog-authored**: 18

## Confidence distribution

- **high**: 158
- **medium**: 150
- **low**: 22

## High-confidence examples

- `prom -> meangirls` | **adjacent-style** | strength 1.152 | distance 0.736
- `meangirls -> prom` | **adjacent-style** | strength 1.152 | distance 0.736
- `spirited -> prom` | **adjacent-style** | strength 1.136 | distance 0.583
- `prom -> spirited` | **adjacent-style** | strength 1.136 | distance 0.583
- `waitress -> ticktick` | **higher-intensity** | strength 1.508 | distance 1.094
- `starsborn -> rocketman` | **higher-intensity** | strength 1.396 | distance 1.147
- `hair -> tommy` | **higher-intensity** | strength 1.198 | distance 0.973
- `moana -> greatest` | **higher-intensity** | strength 1.166 | distance 1.124
- `onceisland -> heights` | **higher-intensity** | strength 1.127 | distance 1.056
- `heights -> hamilton` | **hookier** | strength 1.75 | distance 1.359
- `colorpurple -> deh` | **hookier** | strength 1.75 | distance 1.034
- `lastfive -> deh` | **hookier** | strength 1.75 | distance 1.248
- `matilda -> encanto` | **hookier** | strength 1.75 | distance 1.168
- `prom -> greatest` | **hookier** | strength 1.75 | distance 1.393
- `prom -> hairspray` | **hookier** | strength 1.75 | distance 1.434
- `meangirls -> hairspray` | **hookier** | strength 1.75 | distance 1.606
- `meangirls -> kpop` | **hookier** | strength 1.75 | distance 1.811
- `comefromaway -> hamilton` | **hookier** | strength 1.75 | distance 1.326
- `shrek -> annie` | **hookier** | strength 1.75 | distance 1.596
- `dancerinthedark -> inside` | **hookier** | strength 1.75 | distance 1.548
- `batboy -> littleShop` | **hookier** | strength 1.75 | distance 1.186
- `walkline -> across` | **hookier** | strength 1.67 | distance 1.329
- `walkline -> bohemian` | **hookier** | strength 1.67 | distance 1.119
- `spirited -> greatest` | **hookier** | strength 1.67 | distance 0.978
- `spirited -> hairspray` | **hookier** | strength 1.67 | distance 1.04
- `spirited -> kpop` | **hookier** | strength 1.67 | distance 1.21
- `odessa -> rocky` | **hookier** | strength 1.439 | distance 0.843
- `jamie -> greatest` | **hookier** | strength 1.439 | distance 1.095
- `jamie -> kpop` | **hookier** | strength 1.439 | distance 1.221
- `hedwig -> inside` | **hookier** | strength 1.439 | distance 0.804
- `hedwig -> rocketman` | **hookier** | strength 1.439 | distance 0.92
- `newsies -> hairspray` | **hookier** | strength 1.439 | distance 0.772
- `newsies -> legallyblonde` | **hookier** | strength 1.439 | distance 0.739
- `princessfrog -> encanto` | **hookier** | strength 1.439 | distance 0.968
- `reefer -> littleShop` | **hookier** | strength 1.439 | distance 0.839
- `reefer -> rocky` | **hookier** | strength 1.439 | distance 0.833
- `westside -> wicked` | **lower-friction** | strength 1.53 | distance 1.251
- `chicago -> hairspray` | **lower-friction** | strength 1.53 | distance 0.825
- `starsborn -> beginagain` | **lower-friction** | strength 1.53 | distance 1.885
- `colorpurple -> wicked` | **lower-friction** | strength 1.445 | distance 1.275
- `jcs -> phantom` | **lower-friction** | strength 1.424 | distance 1.062
- `starsborn -> walkline` | **lower-friction** | strength 1.335 | distance 1.261
- `priscilla -> mammamia` | **lower-friction** | strength 1.264 | distance 0.86
- `hedwig -> drhorrible` | **lower-friction** | strength 1.234 | distance 0.845
- `lastfive -> once` | **lower-friction** | strength 1.205 | distance 1.042
- `purplerain -> walkline` | **lower-friction** | strength 1.205 | distance 1.28
- `inside -> ticktick` | **more-belt-forward** | strength 1.75 | distance 0.952
- `cyrano -> phantom` | **more-belt-forward** | strength 1.75 | distance 1.73
- `yesterday -> across` | **more-belt-forward** | strength 1.75 | distance 1.606
- `soundmusic -> annie` | **more-belt-forward** | strength 1.75 | distance 1.284
- `soundmusic -> moana` | **more-belt-forward** | strength 1.75 | distance 1.35
- `grease -> hairspray` | **more-belt-forward** | strength 1.75 | distance 1.042
- `grease -> rockofages` | **more-belt-forward** | strength 1.75 | distance 1.178
- `falsettos -> rent` | **more-belt-forward** | strength 1.75 | distance 1.217
- `singininrain -> chicago` | **more-belt-forward** | strength 1.75 | distance 1.424
- `priscilla -> rocky` | **more-belt-forward** | strength 1.614 | distance 1.099
- `heights -> ticktick` | **more-belt-forward** | strength 1.607 | distance 1.347
- `drhorrible -> ticktick` | **more-belt-forward** | strength 1.607 | distance 0.914
- `mammamia -> hairspray` | **more-belt-forward** | strength 1.607 | distance 0.793
- `mammamia -> rockofages` | **more-belt-forward** | strength 1.607 | distance 1.145

## Low-confidence review queue

- `westside -> lalaland` | wild-card-bridge | strength 0.792 | distance 1.857
- `hamilton -> heights` | wild-card-bridge | strength 0.763 | distance 1.359
- `waitress -> once` | wild-card-bridge | strength 0.697 | distance 1.539
- `comefromaway -> once` | wild-card-bridge | strength 0.685 | distance 1.5
- `wicked -> phantom` | catalog-authored | strength 0 | distance 0.622
- `rockyhorrorlive -> priscilla` | catalog-authored | strength 0 | distance 0.667
- `singstreet -> once` | catalog-authored | strength 0 | distance 0.708
- `singstreet -> beginagain` | catalog-authored | strength 0 | distance 0.747
- `walkline -> beginagain` | catalog-authored | strength 0 | distance 0.801
- `yesterday -> beginagain` | catalog-authored | strength 0 | distance 0.848
- `hamilton -> inside` | catalog-authored | strength 0 | distance 0.91
- `westside -> heights` | catalog-authored | strength 0 | distance 0.922
- `blinded -> beginagain` | catalog-authored | strength 0 | distance 0.999
- `moulin -> odessa` | catalog-authored | strength 0 | distance 1.088
- `waitress -> lastfive` | catalog-authored | strength 0 | distance 1.098
- `kpop -> jamie` | catalog-authored | strength 0 | distance 1.221
- `moulin -> mammamia` | catalog-authored | strength 0 | distance 1.247
- `encanto -> heights` | catalog-authored | strength 0 | distance 1.247
- `wicked -> colorpurple` | catalog-authored | strength 0 | distance 1.275
- `across -> walkline` | catalog-authored | strength 0 | distance 1.329
- `rocketman -> walkline` | catalog-authored | strength 0 | distance 1.42
- `rocketman -> bohemian` | catalog-authored | strength 0 | distance 1.506
