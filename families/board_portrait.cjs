// Give one agent's card a new portrait on a Love Spot page (the page he has open is saved through
// the store; another page through its own file). Usage: node board_portrait.cjs AGENT IMAGE.png PAGE...
const fs = require('fs'), os = require('os'), path = require('path'), crypto = require('crypto');
const { createLoveSpot } = require(path.join(os.homedir(), '.local/lib/excalidraw-local/love-spot-store.cjs'));
const PAGES = path.join(os.homedir(), '.local/share/excalidraw-local/pages');

function swap(scene, agent, fileId, now) {
  // Leader portraits carry the god's tag; the agent's own card shares their group.
  const live = scene.elements.filter(e => !e.isDeleted && !(e.customData && e.customData.live));
  const groups = new Set(live.filter(e => e.type !== 'image' && e.customData && e.customData.agent === agent).flatMap(e => e.groupIds || []));
  const cards = live.filter(e => e.type === 'image' && (e.groupIds || []).some(g => groups.has(g)));
  if (!cards.length) throw Error(`no portrait for ${agent} on "${scene.page ? scene.page.name : '?'}"`);
  return cards.map(e => ({ ...e, fileId, status: 'saved', version: e.version + 1, versionNonce: e.versionNonce + 1, updated: now }));
}

(async () => {
  const [agent, image, ...pages] = process.argv.slice(2);
  const bytes = fs.readFileSync(image), fileId = crypto.createHash('sha1').update(bytes).digest('hex'), now = Date.now();
  const file = { id: fileId, mimeType: 'image/png', dataURL: `data:image/png;base64,${bytes.toString('base64')}`, created: now };
  const board = createLoveSpot();
  try {
    const { scene } = await board.read();
    for (const page of pages) {
      if (scene.page.name === page) {
        const elements = swap(scene, agent, fileId, now);
        await board.save({ type: 'excalidraw', version: 2, source: 'Love Spot', elements, files: { [fileId]: file }, appState: {}, page: scene.page });
      } else {
        const target = path.join(PAGES, `${page}.excalidraw`), saved = JSON.parse(fs.readFileSync(target, 'utf8'));
        const changed = new Map(swap(saved, agent, fileId, now).map(e => [e.id, e]));
        saved.elements = saved.elements.map(e => changed.get(e.id) || e);
        saved.files = { ...(saved.files || {}), [fileId]: file };
        fs.writeFileSync(`${target}.tmp`, JSON.stringify(saved)); fs.renameSync(`${target}.tmp`, target);
      }
      console.log(`${agent} has the new portrait on "${page}"`);
    }
  } finally { board.close(); }
})().catch(e => { console.error(e.message); process.exitCode = 1; });
