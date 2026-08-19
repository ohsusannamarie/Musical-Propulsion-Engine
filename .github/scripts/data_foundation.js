const fs = require('fs');
const vm = require('vm');
const path = require('path');

const root = process.cwd();
const indexPath = path.join(root, 'index.html');
const appPath = path.join(root, 'app.html');
const dataDir = path.join(root, 'data');
fs.mkdirSync(dataDir, { recursive: true });

function extractArrayLiteral(html) {
  const marker = html.match(/const\s+D\s*=\s*/);
  if (!marker) throw new Error('Could not locate const D dataset');
  const start = marker.index + marker[0].length;
  if (html[start] !== '[') throw new Error('const D does not begin with an array');
  let depth = 0, quote = null, escape = false;
  for (let i = start; i < html.length; i++) {
    const ch = html[i];
    if (quote) {
      if (escape) escape = false;
      else if (ch === '\\') escape = true;
      else if (ch === quote) quote = null;
      continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') { quote = ch; continue; }
    if (ch === '[') depth++;
    if (ch === ']') {
      depth--;
      if (depth === 0) return { literal: html.slice(start, i + 1), start, end: i + 1 };
    }
  }
  throw new Error('Could not find end of const D dataset');
}

function safeEvalArray(literal) {
  const sandbox = Object.create(null);
  return vm.runInNewContext('(' + literal + ')', sandbox, { timeout: 2000 });
}

function normalizeTitle(x) {
  if (!x || typeof x !== 'object') throw new Error('Invalid title record');
  if (!x.id || !x.title) throw new Error('Every title requires id and title');
  x.enrichment = x.enrichment || {
    format: null,
    musicalType: null,
    vocalStyle: [],
    lyricalDensity: null,
    musicDrivenPercent: null,
    catharsis: null,
    rewatchability: null,
    familiarityAdvantage: null,
    bestMood: [],
    friction: [],
    gatewaySongs: [],
    notes: null,
    provenance: []
  };
  return x;
}

function collectSources(titles) {
  const keys = ['trailer','soundtrack','imdb','rt','watch','spotify','youtube'];
  const out = {};
  for (const x of titles) {
    const src = {};
    for (const k of keys) if (x[k]) src[k] = x[k];
    if (Object.keys(src).length) out[x.id] = src;
  }
  return { version: 1, generatedFrom: 'inline catalog', sources: out };
}

function validate(titles) {
  if (!Array.isArray(titles) || titles.length < 30) throw new Error(`Catalog unexpectedly small: ${titles.length}`);
  const ids = new Set();
  for (const x of titles) {
    if (ids.has(x.id)) throw new Error(`Duplicate id: ${x.id}`);
    ids.add(x.id);
    if (!x.scores || typeof x.scores !== 'object') throw new Error(`Missing scores: ${x.id}`);
    for (const k of ['propulsion','belt','movement','emotion','comfort','maximalism','narrative','hooks']) {
      if (typeof x.scores[k] !== 'number') throw new Error(`Missing score ${k}: ${x.id}`);
    }
  }
}

let html = fs.readFileSync(indexPath, 'utf8');
const titlesPath = path.join(dataDir, 'titles.json');
let titles;

if (fs.existsSync(titlesPath)) {
  titles = JSON.parse(fs.readFileSync(titlesPath, 'utf8'));
} else {
  const ex = extractArrayLiteral(html);
  titles = safeEvalArray(ex.literal);
}

titles = titles.map(normalizeTitle);
validate(titles);

fs.writeFileSync(titlesPath, JSON.stringify(titles, null, 2) + '\n');

const schema = {
  schemaVersion: '1.0.0',
  required: ['id','title','scores'],
  scoreDimensions: ['propulsion','belt','movement','emotion','comfort','maximalism','narrative','hooks'],
  enrichmentFields: {
    format: 'film | stage-capture | animated | biopic | musical-adjacent | other',
    musicalType: 'original | jukebox | biographical | adaptation | filmed-stage | hybrid',
    vocalStyle: 'array of descriptors',
    lyricalDensity: '1-5 or null',
    musicDrivenPercent: '0-100 or null',
    catharsis: '1-5 or null',
    rewatchability: '1-5 or null',
    familiarityAdvantage: '1-5 or null',
    bestMood: 'array of mood tags',
    friction: 'array of potential mismatch notes',
    gatewaySongs: 'ranked song objects',
    notes: 'analytical notes',
    provenance: 'source records for researched facts'
  }
};
fs.writeFileSync(path.join(dataDir, 'schema.json'), JSON.stringify(schema, null, 2) + '\n');

const relPath = path.join(dataDir, 'relationships.json');
if (!fs.existsSync(relPath)) fs.writeFileSync(relPath, JSON.stringify({ version: 1, relationships: [] }, null, 2) + '\n');
fs.writeFileSync(path.join(dataDir, 'sources.json'), JSON.stringify(collectSources(titles), null, 2) + '\n');

const readme = `# Musical Propulsion Engine data\n\nThis directory is the source of truth for catalog enrichment.\n\n- \`titles.json\`: title records and analytical fingerprints\n- \`relationships.json\`: explicit title-to-title bridges that supplement computed similarity\n- \`sources.json\`: external media and reference URLs separated from taste analysis\n- \`schema.json\`: current enrichment contract\n\nThe deployed HTML still receives an inline \`const D\` at build time for reliability on GitHub Pages. Edit the structured data here, then run the Data Foundation workflow to validate and bake the catalog into \`index.html\` and \`app.html\`.\n`;
fs.writeFileSync(path.join(dataDir, 'README.md'), readme);

function bake(file) {
  let body = fs.readFileSync(file, 'utf8');
  const ex = extractArrayLiteral(body);
  const literal = JSON.stringify(titles);
  body = body.slice(0, ex.start) + literal + body.slice(ex.end);
  fs.writeFileSync(file, body);
}

bake(indexPath);
if (fs.existsSync(appPath)) bake(appPath);

console.log(`Data Foundation ready: ${titles.length} titles validated and baked.`);
