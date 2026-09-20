/**
 * Render screenshot checkpoints of desmos_state.json with Playwright.
 *
 *   npm install            (once, installs playwright-core)
 *   npx playwright-core install chromium   (once)
 *   node scripts/render_checkpoints.js [outDir] [T1 T2 ...]
 *
 * Loads the state into desmos.com/3d headlessly, sets the master clock T,
 * and saves one PNG of the graph area per checkpoint.
 * No Desmos account or credentials are used.
 */
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const outDir = path.resolve(process.argv[2] || path.join(root, 'assets/screenshots/checkpoints'));
const checkpoints = process.argv.length > 3
  ? process.argv.slice(3).map(Number)
  : [1, 7, 9.6, 10.4, 12, 15];

(async () => {
  const state = JSON.parse(fs.readFileSync(path.join(root, 'desmos_state.json'), 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });

  // Use the real GPU where possible: software rendering clamps line widths below 1, so the hairline
  // fabric would look heavy. Background throttling is disabled so timings are stable.
  const gpuArgs = process.platform === 'win32' ? ['--use-angle=d3d11'] : [];
  const browser = await chromium.launch({
    args: [...gpuArgs, '--ignore-gpu-blocklist', '--enable-gpu-rasterization',
           '--disable-renderer-backgrounding', '--disable-background-timer-throttling',
           '--disable-backgrounding-occluded-windows'],
  });
  const page = await browser.newPage({ viewport: { width: 1200, height: 800 } });
  await page.goto('https://www.desmos.com/3d', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.Calc, null, { timeout: 30000 });
  await page.evaluate((s) => Calc.setState(s), state);

  const bad = await page.evaluate(() =>
    Calc.getExpressions().filter((e) => e.error).map((e) => `${e.id}: ${e.error}`));
  if (bad.length) console.warn('Expression errors:\n  ' + bad.join('\n  '));

  for (const T of checkpoints) {
    await page.evaluate((t) => Calc.setExpression({ id: 'time_T', latex: `T=${t}` }), T);
    await page.waitForTimeout(2500);
    const file = path.join(outDir, `T${String(T).replace('.', '_')}.png`);
    await page.screenshot({ path: file, clip: { x: 400, y: 46, width: 800, height: 754 } });
    console.log('saved', file);
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
