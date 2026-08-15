@@ -9,9 +9,15 @@
 
 import json
 import os
 import sys
 from pathlib import Path
 from typing import Any
 
 BASE_DIR = Path(__file__).resolve().parent
 # Ensure sibling imports work even when launched via absolute path / wrappers.
 if str(BASE_DIR) not in sys.path:
     sys.path.insert(0, str(BASE_DIR))
@@ -26,10 +32,21 @@
 
 mcp = FastMCP("fiction-reverse-engineering")
 
 BASE_DIR = Path(__file__).resolve().parent
-FORMULAS_DIR = Path(
-    os.environ.get("FICTION_RE_FORMULAS_DIR", str(BASE_DIR / "formulas"))
-)
+REPO_ROOT = BASE_DIR.parent.parent
+
+
+def _resolve_formulas_dir() -> Path:
+    raw = os.environ.get("FICTION_RE_FORMULAS_DIR")
+    if not raw:
+        return BASE_DIR / "formulas"
+    path = Path(raw)
+    if path.is_absolute():
+        return path
+    # Relative env values are repo-root-relative (see run.sh / mcp.json).
+    return (REPO_ROOT / path).resolve()
+
+
+FORMULAS_DIR = _resolve_formulas_dir()
 FORMULAS_DIR.mkdir(parents=True, exist_ok=True)
 
 
@@ -199,4 +216,4 @@ def list_available_formulas() -> str:
 
 
 if __name__ == "__main__":
-    mcp.run()
+    mcp.run(transport="stdio")
