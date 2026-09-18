/**
 * Desmos 3D Binary Singularity Merger Loader
 * 
 * Instructions:
 * 1. Navigate to https://www.desmos.com/3d in any modern web browser.
 * 2. Open Developer Tools Console (F12 or Ctrl+Shift+I).
 * 3. Paste and run this script to inject the complete binary merger simulation.
 */

(async function loadDesmosBinaryMerger() {
  if (typeof Calc === 'undefined') {
    console.error('Error: Desmos Calc object not found. Ensure you are on https://www.desmos.com/3d');
    return;
  }

  const rawUrl = 'https://raw.githubusercontent.com/0xh1tesh/binary-singularity-simulation/main/desmos_state.json';
  try {
    console.log('Fetching simulation state from GitHub...');
    const res = await fetch(rawUrl);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const state = await res.json();
    Calc.setState(state, { allowUndo: true });
    console.log('✅ Desmos 3D Binary Singularity Merger simulation loaded successfully!');
  } catch (err) {
    console.warn('Could not fetch from remote URL. Falling back to local state paste.');
  }
})();
