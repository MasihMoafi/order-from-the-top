// Render the current Love Spot page to an SVG file (rectangles, text, images, opacity) for a
// headless check of what the live board shows. Usage: node board_snap.cjs OUT.svg
const fs = require('fs'), os = require('os'), path = require('path');
const { createLoveSpot } = require(path.join(os.homedir(), '.local/lib/excalidraw-local/love-spot-store.cjs'));
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
(async () => {
  const board = createLoveSpot();
  try {
    const { scene } = await board.read();
    const els = scene.elements.filter(e => !e.isDeleted);
    const x0 = Math.min(...els.map(e => e.x)) - 20, y0 = Math.min(...els.map(e => e.y)) - 20;
    const x1 = Math.max(...els.map(e => e.x + (e.width || 0))) + 20, y1 = Math.max(...els.map(e => e.y + (e.height || 0))) + 20;
    const out = [`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${x0} ${y0} ${x1 - x0} ${y1 - y0}" width="${Math.round((x1 - x0) / 2)}"><rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" fill="white"/>`];
    for (const e of els) {
      const op = (e.opacity ?? 100) / 100;
      if (e.type === 'rectangle' || e.type === 'ellipse') {
        const fill = e.backgroundColor === 'transparent' ? 'none' : e.backgroundColor;
        out.push(`<rect x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" rx="${e.roundness ? 8 : 0}" fill="${fill}" stroke="${e.strokeColor}" opacity="${op}"/>`);
      } else if (e.type === 'image') {
        const f = scene.files && scene.files[e.fileId];
        if (f) out.push(`<image href="${f.dataURL}" x="${e.x}" y="${e.y}" width="${e.width}" height="${e.height}" opacity="${op}"/>`);
      } else if (e.type === 'text') {
        e.text.split('\n').forEach((line, i) => out.push(`<text x="${e.x}" y="${e.y + (i + 1) * e.fontSize * 1.2}" font-size="${e.fontSize}" font-family="monospace" fill="${e.strokeColor}" opacity="${op}">${esc(line)}</text>`));
      } else if (e.type === 'arrow' || e.type === 'line') {
        out.push(`<polyline points="${e.points.map(p => `${e.x + p[0]},${e.y + p[1]}`).join(' ')}" fill="none" stroke="${e.strokeColor}" stroke-width="2" opacity="${op}"/>`);
      }
    }
    out.push('</svg>');
    fs.writeFileSync(process.argv[2], out.join('\n'));
    console.log(`wrote ${process.argv[2]} (${els.length} elements, page "${scene.page.name}")`);
  } finally { board.close(); }
})().catch(e => { console.error(e.message); process.exitCode = 1; });
