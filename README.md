# The Musical Propulsion Engine

https://ohsusannamarie.github.io/Musical-Propulsion-Engine/

A mobile-first musical discovery app built around **propulsion**, **belt instinct**, **body movement**, **emotional amplitude**, **musical DNA**, and the exact thing you want more of.

## Current build

**v2.2.1**

Highlights:
- Rabbit Hole discovery: **I loved ___ → give me more of ___**
- Tonight / Press Play mode
- Explainable recommendation bridges
- Gateway songs with Spotify discovery links
- Trailer, IMDb, Rotten Tomatoes, and Where to Watch actions
- Editable personal library statuses stored locally in the browser
- Mobile-safe navigation drawer
- Real poster/media treatment with graceful stylized fallbacks

## GitHub Pages

The repository root contains the Pages entry point. The full static application is stored as four compressed text payloads under `app/`; `index.html` loads and expands them in the browser. This keeps the site fully static and GitHub-Pages-friendly while preserving the complete single-file app.

Publish from **main / (root)** in Settings → Pages.

## State

Library changes use browser `localStorage`, so they persist per browser/device. No backend is required.
