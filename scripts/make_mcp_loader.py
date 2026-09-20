"""Write .playwright-mcp/load_state.js: a Playwright-MCP `browser_run_code_unsafe` snippet that loads
desmos_state.json into the open desmos.com/3d page, sets T (default from argv), and reports errors.

Usage: python scripts/make_mcp_loader.py [T]
"""
import json, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
state = json.loads((root / "desmos_state.json").read_text(encoding="utf-8"))
T = sys.argv[1] if len(sys.argv) > 1 else "1"
code = """async (page) => {
  const st = %s;
  await page.setViewportSize({ width: 1200, height: 800 });
  await page.evaluate(s => Calc.setState(s), st);
  await page.evaluate(t => Calc.setExpression({ id: 'time_T', latex: 'T=' + t }), '%s');
  await page.waitForTimeout(2500);
  return await page.evaluate(() => ({
    n: Calc.getExpressions().length,
    errors: Calc.getExpressions().filter(e => e.error).map(e => e.id + ': ' + e.error)
  }));
}""" % (json.dumps(state), T)
out = root / ".playwright-mcp" / "load_state.js"
out.parent.mkdir(exist_ok=True)
out.write_text(code, encoding="utf-8")
print("wrote", out, len(code), "bytes")
