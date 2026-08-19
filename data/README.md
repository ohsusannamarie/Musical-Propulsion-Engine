# Musical Propulsion Engine data

This directory is the source of truth for catalog enrichment.

- `titles.json`: title records and analytical fingerprints
- `relationships.json`: explicit title-to-title bridges that supplement computed similarity
- `sources.json`: external media and reference URLs separated from taste analysis
- `schema.json`: current enrichment contract

The deployed HTML still receives an inline `const D` at build time for reliability on GitHub Pages. Edit the structured data here, then run the Data Foundation workflow to validate and bake the catalog into `index.html` and `app.html`.
