/**
 * Measure real playback frame rate of desmos_state.json.
 *
 *   node scripts/bench_fps.js [seconds]
 *
 * Loads the state into desmos.com/3d in a GPU-backed Chromium (background throttling disabled), presses
 * the real Play button on T and counts completed 3D redraws per second. Prints redraws/s.
 */
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const seconds = Number(process.argv[2]) || 6;
const state = JSON.parse(fs.readFileSync(path.resolve(__dirname, '..', 'desmos_state.json'), 'utf8'));

(async () => {
  const gpuArgs = process.platform === 'win32' ? ['--use-angle=d3d11'] : [];
  const browser = await chromium.launch({
    args: [...gpuArgs, '--ignore-gpu-blocklist', '--enable-gpu-rasterization',
           '--disable-renderer-backgrounding', '--disable-background-timer-throttling',
           '--disable-backgrounding-occluded-windows'],
  });
  const page = await browser.newPage({ viewport: { width: 1200, height: 800 } });
  await page.goto('https://www.desmos.com/3d', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.Calc, null, { timeout: 30000 });
  const gpu = await page.evaluate(() => {
    const gl = document.createElement('canvas').getContext('webgl2');
    const d = gl.getExtension('WEBGL_debug_renderer_info');
    return d ? gl.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'unknown';
  });
  await page.evaluate((s) => Calc.setState(s), state);
  await page.waitForTimeout(2500);
  const bad = await page.evaluate(() => Calc.getExpressions().filter((e) => e.error).map((e) => e.id));
  if (bad.length) console.warn('Expression errors:', bad.join(', '));

  await page.evaluate(() => Calc.setExpression({ id: 'time_T', latex: 'T=0' }));
  await page.waitForTimeout(1200);
  await page.getByRole('button', { name: 'Play T Animation' }).click();
  await page.waitForTimeout(1500);
  const redraws = () => page.evaluate(() => Calc.controller.getGrapher3d().lastCompletedRedrawId);
  const a = await redraws();
  const t0 = Date.now();
  await page.waitForTimeout(seconds * 1000);
  const b = await redraws();
  const fps = (b - a) / ((Date.now() - t0) / 1000);
  console.log(`GPU: ${gpu}`);
  console.log(`redraws per second during playback: ${fps.toFixed(1)}`);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
