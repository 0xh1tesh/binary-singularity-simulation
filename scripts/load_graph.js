/**
 * Desmos 3D Binary Singularity Merger Loader
 *
 * 1. Open https://www.desmos.com/3d in a desktop browser.
 * 2. Open the Developer Tools console (F12 or Ctrl+Shift+I).
 * 3. Paste and run this script. It fetches desmos_state.json, checks it,
 *    loads it with Calc.setState and reports whether the graph evaluated cleanly.
 */
(async function loadDesmosBinaryMerger() {
  const rawUrl = 'https://raw.githubusercontent.com/0xh1tesh/binary-singularity-simulation/main/desmos_state.json';

  if (typeof Calc === 'undefined') {
    console.error('[loader] Desmos "Calc" not found. Open https://www.desmos.com/3d first, then re-run.');
    return;
  }

  let state;
  try {
    const res = await fetch(rawUrl, { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
    state = await res.json();
  } catch (err) {
    console.error(`[loader] Could not fetch the state (${err.message}).\n` +
      '  - Check your connection and that the URL is reachable:\n    ' + rawUrl + '\n' +
      '  - Or open desmos_state.json locally, copy its contents and run: Calc.setState(<paste>)');
    return;
  }

  const list = state && state.expressions && state.expressions.list;
  const ids = new Set((list || []).map((e) => e.id));
  const required = ['time_T', 'time_Tm', 'func_ztotal', 'grid_lines_x', 'grid_lines_y'];
  const missing = required.filter((id) => !ids.has(id));
  if (!Array.isArray(list) || missing.length) {
    console.error('[loader] The fetched state looks invalid' +
      (missing.length ? `; missing expressions: ${missing.join(', ')}` : '') + '. Nothing was loaded.');
    return;
  }

  try {
    Calc.setState(state, { allowUndo: true });
  } catch (err) {
    console.error(`[loader] Calc.setState failed: ${err.message}`);
    return;
  }

  // Give Desmos a moment to evaluate, then report any expression errors.
  setTimeout(() => {
    const errors = Calc.getExpressions().filter((e) => e.error).map((e) => `${e.id}: ${e.error}`);
    if (errors.length) console.warn('[loader] Loaded, but some expressions have errors:\n  ' + errors.join('\n  '));
    else console.log(`[loader] Loaded ${list.length} expressions with no errors. Press play on T.`);
  }, 1500);
})();
