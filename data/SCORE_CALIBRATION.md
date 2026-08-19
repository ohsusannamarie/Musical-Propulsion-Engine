# Score Calibration Report

Catalog: **81 titles**

Editorial scores are preserved in `scoresRaw`. The live `scores` field is now percentile-calibrated so recommendation math has more separation while preserving within-dimension ordering.

| Dimension | Raw mean | Calibrated mean | Raw stdev | Calibrated stdev | Raw ≥4.5 | Calibrated ≥4.5 |
|---|---:|---:|---:|---:|---:|---:|
| propulsion | 4.42 | 3.5 | 0.47 | 0.99 | 47 | 19 |
| belt | 4.55 | 3.51 | 0.45 | 0.99 | 58 | 23 |
| movement | 4.3 | 3.5 | 0.6 | 0.99 | 37 | 23 |
| emotion | 4.47 | 3.51 | 0.52 | 0.99 | 46 | 24 |
| comfort | 3.79 | 3.5 | 1.0 | 0.99 | 26 | 17 |
| maximalism | 4.4 | 3.5 | 0.64 | 0.99 | 51 | 17 |
| narrative | 4.51 | 3.51 | 0.51 | 0.99 | 52 | 25 |
| hooks | 4.68 | 3.51 | 0.33 | 0.99 | 63 | 26 |
| afterglow | 4.69 | 3.51 | 0.3 | 0.99 | 65 | 25 |
| replay | 4.59 | 3.51 | 0.43 | 0.99 | 56 | 25 |
