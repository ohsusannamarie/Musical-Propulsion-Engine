# Media Recovery Status

- Catalog titles: **81**
- Bundled: **72** (88.9%)
- Remote: **0** (0.0%)
- Fallback: **0** (0.0%)
- Missing: **9** (11.1%)

## Recovery queue

- `hedwigstage` — Hedwig and the Angry Inch: Broadway (2014)
- `batboy` — Bat Boy: The Musical (2004)
- `singininrain` — Singin’ in the Rain (1952)
- `cabaret` — Cabaret (1972)
- `rockyhorrorlive` — The Rocky Horror Picture Show: Let’s Do the Time Warp Again (2016)
- `billyelliot` — Billy Elliot the Musical Live (2014)
- `tickstage` — tick, tick... BOOM! Off-Broadway Recording (2001)
- `onceisland` — Once on This Island (2018)
- `shocktreatment` — Shock Treatment (1981)

## Policy

Poster state is explicit and durable: `bundled`, `remote`, `fallback`, or `missing`. CI never downloads remote art as a prerequisite for deployment. Recovery happens separately, then the manifest is rebuilt.
