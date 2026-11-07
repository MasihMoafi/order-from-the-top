// Paint one game frame onto a Love Spot page: dead agents fade, each card shows its points and
// the move it just played (C green, D red; red LIE when it promised C and played D); a dying card
// flashes red for its last round. Beside the board: what each family said, and the round's events.
// Usage: node board_live.cjs FRAME.json   (written by board_watch.py or board_replay.py)
// frame.page names the page (default "Families"). A missing page is made as a copy of the
// Families cards. The painter never takes the board from another page he is looking at.
const fs = require('fs'), os = require('os'), path = require('path');
const { createLoveSpot } = require(path.join(os.homedir(), '.local/lib/excalidraw-local/love-spot-store.cjs'));
const PAGES = path.join(os.homedir(), '.local/share/excalidraw-local/pages');
const MOVE_COLOUR = { C: '#2f9e44', D: '#e03131' };

function base(id, type, now) {
  return {
    id, type, angle: 0, strokeColor: '#16191c', backgroundColor: 'transparent', fillStyle: 'solid',
    strokeWidth: 2, strokeStyle: 'solid', roughness: 0, opacity: 100, groupIds: [], frameId: null, roundness: null,
    seed: 7, version: 0, versionNonce: 0, isDeleted: false, boundElements: null, link: null, locked: true,
    updated: now, customData: { live: true },
  };
}

// A clock-based version always beats the copy an open window holds; a plain +1 can tie with it,
// and on a tie the window keeps its own (seen 7 Nov: an old feed stayed on screen).
function bump(e, now, changes) {
  return { ...e, ...changes, version: Math.max(e.version + 1, Math.floor(now / 100)), versionNonce: e.versionNonce + 1, updated: now };
}

function textEl(id, x, y, text, size, old, now, colour = '#16191c') {
  const lines = text.split('\n');
  const width = Math.max(...lines.map(l => l.length)) * size * 0.6 + 8, height = lines.length * size * 1.25;
  const start = old || { ...base(id, 'text', now), fontFamily: 3, textAlign: 'left', verticalAlign: 'top',
    containerId: null, autoResize: true, lineHeight: 1.25 };
  return bump(start, now, { x, y, width, height, fontSize: size, text, originalText: text, strokeColor: colour, isDeleted: false });
}

function wrap(text, width, lines) {
  const words = text.replace(/\s+/g, ' ').trim().split(' '), out = [''];
  for (const w of words) {
    if ((out[out.length - 1] + ' ' + w).trim().length > width) out.push('');
    out[out.length - 1] = (out[out.length - 1] + ' ' + w).trim();
  }
  return out.length > lines ? [...out.slice(0, lines - 1), out[lines - 1].slice(0, width - 1) + '…'] : out;
}

async function openPage(board, name) {
  let { scene } = await board.read();
  if (scene.page.name === name) return scene;
  const file = path.join(PAGES, `${name}.excalidraw`);
  if (name === 'Families' || fs.existsSync(file)) return null; // he is looking at another page
  // First replay: a copy of the Families cards without the live layer.
  const families = JSON.parse(fs.readFileSync(path.join(PAGES, 'Families.excalidraw'), 'utf8'));
  scene = (await board.changePage({ action: 'new', name })).scene;
  const elements = families.elements.filter(e => !e.isDeleted && !(e.customData && e.customData.live));
  scene = (await board.save({ type: 'excalidraw', version: 2, source: 'Love Spot', elements, files: families.files || {}, appState: {}, page: scene.page })).scene;
  return scene;
}

(async () => {
  const snap = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const page = snap.page || 'Families';
  const board = createLoveSpot();
  try {
    const scene = await openPage(board, page);
    if (!scene) { console.log(`skipped: Love Spot shows another page, not "${page}"`); return; }
    // byId includes deleted elements: a word deleted last round comes back as its next version.
    const live = scene.elements.filter(e => !e.isDeleted), byId = new Map(scene.elements.map(e => [e.id, e])), now = Date.now();
    const out = [], card = new Map();
    for (const e of live) {
      const aid = e.customData && e.customData.agent;
      if (!aid || e.customData.live || !(e.type === 'rectangle' || e.type === 'image')) continue;
      const best = card.get(aid);
      if (!best || e.width * e.height > best.width * best.height) card.set(aid, e);
    }
    if (!card.size) throw Error(`no agent cards on page "${page}"`);
    const xs = [...card.values()];
    const minX = Math.min(...xs.map(c => c.x)), minY = Math.min(...xs.map(c => c.y));
    const maxX = Math.max(...xs.map(c => c.x + c.width));
    const keep = new Set();
    const died = new Set(snap.died || []), broke = new Set((snap.talk || []).filter(t => t.broke).map(t => t.sender));
    for (const [aid, c] of card) {
      const a = snap.agents[aid];
      if (!a) continue;
      const opacity = a.alive ? 100 : 18, group = new Set(c.groupIds || []);
      for (const e of live.filter(e => e.id === c.id || (e.groupIds || []).some(g => group.has(g)))) {
        if (e.opacity !== opacity && !(e.customData && e.customData.live)) out.push(bump(e, now, { opacity }));
      }
      const move = (snap.moves || {})[aid], lie = broke.has(aid);
      const label = a.alive ? `${aid} ${Math.round(a.score * 10) / 10}${move ? ' ' + move : ''}${lie ? ' LIE' : ''}` : `${aid} dead`;
      const size = Math.max(10, Math.round(c.width / 7)), sid = `live-score-${aid}`;
      const y = aid === 'P01' ? c.y - size * 1.4 : c.y + c.height + 2; // the god's own name sits below its card
      out.push(textEl(sid, c.x, y, label, size, byId.get(sid), now, !a.alive ? '#868e96' : lie ? '#e03131' : MOVE_COLOUR[move] || '#16191c'));
      keep.add(sid);
      if (a.alive && move) { // the move shows at any zoom: a green or red frame; dashed red for a broken promise
        const id = `live-move-${aid}`, pad = Math.max(5, c.width / 12), old = byId.get(id);
        out.push(bump(old || base(id, 'rectangle', now), now, { x: c.x - pad, y: c.y - pad, width: c.width + 2 * pad,
          height: c.height + 2 * pad, strokeColor: lie ? '#e03131' : MOVE_COLOUR[move], strokeWidth: Math.max(4, c.width / 14),
          strokeStyle: lie ? 'dashed' : 'solid', backgroundColor: 'transparent', opacity: 100, isDeleted: false }));
        keep.add(id);
      }
      if (died.has(aid)) { // the round it dies, the card flashes red
        const id = `live-dead-${aid}`, old = byId.get(id);
        const flash = old || { ...base(id, 'rectangle', now), fillStyle: 'solid' };
        out.push(bump(flash, now, { x: c.x - 4, y: c.y - 4, width: c.width + 8, height: c.height + 8,
          backgroundColor: '#e03131', strokeColor: '#c92a2a', strokeWidth: 4, opacity: 55, isDeleted: false }));
        keep.add(id);
      }
    }
    // Beside the board: what each family said this round, a promise of C followed by D in red.
    const panelX = maxX + 120, panelSize = 26, panelWidth = 62, shown = 4;
    let y = minY, n = 0;
    const order = ['P01', 'P02', 'P17', 'P32', 'P47', 'P62'];
    const names = { P01: 'God', P02: 'Octopus family', P17: 'Mafia family', P32: 'President family', P47: 'Bishop family', P62: 'Zeus family' };
    const put = (text, colour, size = panelSize) => {
      const id = `live-say-${n++}`;
      out.push(textEl(id, panelX, y, text, size, byId.get(id), now, colour)); keep.add(id);
      y += text.split('\n').length * size * 1.25 + 4;
    };
    if (snap.talk) {
      put('Who said what (red: promised C, played D)', '#16191c', 34); y += 12;
      for (const fam of order) {
        const lines = snap.talk.filter(t => t.family === fam);
        if (!lines.length) continue;
        put(names[fam], '#16191c', 30);
        for (const t of lines.slice(0, shown)) {
          const said = `${t.sender} ${t.line}` + (t.played ? `  [played ${t.played}]` : '');
          put(wrap(said, panelWidth, 2).join('\n'), t.broke ? '#e03131' : '#1971c2');
        }
        if (lines.length > shown) put(`(+${lines.length - shown} more)`, '#868e96');
        y += 16;
      }
    }
    for (const e of live) { // last round's words, flashes and old arrows go away
      if (e.customData && e.customData.live && /^live-(say|talk|dead|move)-/.test(e.id) && !keep.has(e.id)) out.push(bump(e, now, { isDeleted: true }));
    }
    const header = `Stage ${snap.stage} | round ${snap.round}` + (snap.variant ? ` | ${snap.variant}` : '') +
      ` | entry fee ${snap.ante} | alive ${snap.alive}/${snap.total}` + (snap.outcome ? ` | END: ${snap.outcome}` : '');
    out.push(textEl('live-header', minX, minY - 110, header, 56, byId.get('live-header'), now));
    // Under the words: deaths and treaties first, then who took points from whom (reasons are in the log).
    const short = f => f.replace(/^(\S+ took points from \S+):.*/, '$1');
    const events = [...snap.feed.filter(f => !/took points/.test(f)), ...snap.feed.filter(f => /took points/.test(f))].map(short);
    const lines = events.flatMap(f => wrap(f, 62, 1));
    const feed = ['This round', ...lines.slice(0, 16), ...(lines.length > 16 ? [`(+${lines.length - 16} more)`] : [])].join('\n');
    out.push(textEl('live-feed', panelX, y + 20, events.length ? feed : 'This round: no deaths, no treaties', 24, byId.get('live-feed'), now));
    await board.save({ type: 'excalidraw', version: 2, source: 'Love Spot', elements: out, files: {}, appState: {}, page: scene.page });
    console.log(`painted ${out.length} items on "${page}"`);
  } finally { board.close(); }
})().catch(e => { console.error(e.message); process.exitCode = 1; });
