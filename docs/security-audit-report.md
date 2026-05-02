# Security Audit Report: BMAD Method A0 Plugin

**Date:** 2026-05-02
**Auditor:** Security Auditor (Agent Zero)
**Scope:** Full codebase — 5 dimensions (Input Handling, Auth, Data Protection, Infrastructure, Third-Party)
**Codebase Version:** 1.3.0

---

## Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High     | 1 |
| Medium   | 3 |
| Low      | 3 |
| Info     | 4 |

---

## Findings

### [HIGH] CSS Class Injection via Unsanitized `DATA.grade` in BMB Report Generators

- **Location:** `skills/bmad-bmb/workflows/agent/scripts/generate-html-report.py:237` and `skills/bmad-bmb/workflows/workflow/scripts/generate-html-report.py:254`
- **Description:** The `DATA.grade` value from `report-data.json` is interpolated directly into a CSS class attribute without sanitization via the `esc()` function. The text content is sanitized, but the class name is not:
  ```javascript
  document.getElementById('grade-area').innerHTML =
    `<div class="grade grade-${DATA.grade}">${esc(DATA.grade)}</div>`;
  ```
  While `esc()` is used for the text node, `DATA.grade` in the class attribute is raw. A crafted `report-data.json` with grade `"A"><img src=x onerror=alert(1)` would break out of the class attribute and inject arbitrary HTML.
- **Impact:** Stored XSS via a maliciously crafted `report-data.json` file. An attacker who can control the report data file can execute arbitrary JavaScript in the browser context when the HTML report is opened. This could lead to credential theft or arbitrary actions in the browser.
- **Proof of Concept:**
  1. Create a `report-data.json` with `{"grade": "A\"><img src=x onerror=alert(document.cookie)>"}`
  2. Run `python3 generate-html-report.py <report-dir> --open`
  3. The rendered HTML will contain the injected `<img>` tag in the grade div
- **Recommendation:** Sanitize `DATA.grade` before using it in the class attribute, or restrict it to an allowlist of known values:
  ```javascript
  // Option A: Allowlist (preferred)
  const VALID_GRADES = ['A', 'B', 'C', 'D', 'F'];
  const grade = VALID_GRADES.includes(DATA.grade) ? DATA.grade : 'unknown';
  document.getElementById('grade-area').innerHTML =
    `<div class="grade grade-${grade}">${esc(DATA.grade)}</div>`;
  
  // Option B: Strip non-alphanumeric
  const grade = DATA.grade.replace(/[^a-zA-Z0-9_-]/g, '');
  ```

---

### [MEDIUM] `shell=True` in `subprocess.run` for Windows `start` Command

- **Location:** `skills/bmad-bmb/workflows/agent/scripts/generate-html-report.py:529`, `skills/bmad-bmb/workflows/workflow/scripts/generate-html-report.py:533`, `skills/bmad-bmb/workflows/workflow/scripts/generate-convert-report.py:400`
- **Description:** All three BMB report generators use `subprocess.run(['start', str(output_path)], shell=True)` as a fallback for Windows. The `output_path` is derived from `argparse` user input (the report directory argument) and is passed through `shell=True`.
  ```python
  subprocess.run(['start', str(output_path)], shell=True)
  ```
- **Impact:** On Windows, a user-controlled path string containing shell metacharacters (e.g., `& calc`) could execute arbitrary commands. This requires local execution of the script with a crafted argument. The vulnerability is Windows-specific and requires interactive local access.
- **Recommendation:** Use `os.startfile()` on Windows instead, or construct the command safely:
  ```python
  import os, sys, subprocess
  if sys.platform == 'win32':
      os.startfile(str(output_path))  # No shell involved
  elif sys.platform == 'darwin':
      subprocess.run(['open', str(output_path)])
  else:
      subprocess.run(['xdg-open', str(output_path)])
  ```

---

### [MEDIUM] Error Message Information Disclosure in API Endpoint

- **Location:** `api/_bmad_status.py:88`
- **Description:** The `_bmad_status` API endpoint catches all exceptions and returns the raw exception string to the client:
  ```python
  except Exception as e:
      return {"success": False, "error": str(e)}
  ```
  This can expose internal file paths, Python tracebacks, or database connection details in error messages.
- **Impact:** An attacker can probe the API to trigger errors and learn about the server's internal structure, file system layout, or software versions. This information aids in crafting targeted attacks.
- **Recommendation:** Return a generic error message to the client and log the full details server-side:
  ```python
  except Exception as e:
      log.error("BMAD status API error: %s", traceback.format_exc())
      return {"success": False, "error": "Internal error — check server logs"}
  ```

---

### [MEDIUM] Glob Pattern Injection via YAML `outputs` Field

- **Location:** `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py:261-263`
- **Description:** The `outputs` field from `module.yaml` files is used directly as a glob pattern without validation:
  ```python
  pattern = wf.get("outputs", "").strip()
  if pattern and pattern != "*":
      matches = list(resolved_dir.glob(pattern))
  ```
  A crafted `module.yaml` with `outputs: "**/*.py"` or `outputs: "../../**/*"` could scan unintended directories. Python's `Path.glob()` does not allow escaping the base path with `..`, but `**/*.py` would recursively scan all subdirectories.
- **Impact:** An attacker who can control a `module.yaml` file could cause excessive filesystem scanning (DoS) or discover file names in directories below the target. The glob results are only used as boolean existence checks, so data exfiltration is limited to file names in staleness warnings. The `module.yaml` files are plugin-bundled (not user-writable) in normal operation, reducing practical exploitability.
- **Recommendation:** Validate the glob pattern to prevent traversal and overly broad patterns:
  ```python
  def _safe_glob_pattern(pattern: str) -> str:
      """Sanitize a glob pattern from YAML to prevent traversal/wildcard abuse."""
      if '..' in pattern or pattern.startswith('/'):
          return '*.md'  # Fallback to safe default
      if '**' in pattern:
          return '*.md'  # Prevent recursive scanning
      return pattern
  ```

---

### [LOW] BMB Report Generators Use `innerHTML` with User-Derived Data

- **Location:** `skills/bmad-bmb/workflows/agent/scripts/generate-html-report.py:233-435` and `skills/bmad-bmb/workflows/workflow/scripts/generate-html-report.py:251-408`
- **Description:** The BMB report generators use `innerHTML` extensively (10 instances in agent script, 8 in workflow script) to render report data. While the `esc()` helper function is used consistently for text content (37 and 28 calls respectively), the pattern of building HTML strings with string interpolation is inherently fragile.
- **Impact:** If a developer adds a new rendering function and forgets to use `esc()`, it creates an XSS vector. This is a defense-in-depth concern, not an active vulnerability.
- **Recommendation:** Consider using a template library or DOM API (`createElement`, `textContent`) instead of string-based HTML construction. At minimum, add a comment to each `innerHTML` assignment reminding developers to use `esc()`.

---

### [LOW] Cache Eviction Uses FIFO Without Size Limit on Individual Entries

- **Location:** `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py:47-53`
- **Description:** The `_evict_if_full` function evicts the oldest half of entries when the cache exceeds `_MAX_CACHE_ENTRIES` (128). However, there's no limit on the size of individual cache entries. A crafted YAML file with extremely large content could consume significant memory.
- **Impact:** Memory exhaustion if a maliciously large YAML file is placed in the skills directory. Requires write access to the plugin directory.
- **Recommendation:** Add a size check on parsed YAML data:
  ```python
  _MAX_ENTRY_SIZE = 1_000_000  # 1MB
  parsed = yaml.safe_load(text)
  if parsed and len(str(parsed)) > _MAX_ENTRY_SIZE:
      log.warning("BMAD routing: skipping oversized YAML: %s", yaml_path)
      return {}
  ```

---

### [LOW] Path Construction in `_parse_alias_map` Trusts Markdown Table Content

- **Location:** `extensions/python/message_loop_prompts_after/_80_bmad_routing_manifest.py:179-214`
- **Description:** The `_parse_alias_map` function parses path conventions from `01-bmad-config.md` (a Markdown table). The parsed paths are used directly in `Path()` construction. While the config file is generated by `bmad-init.sh` and not normally user-editable, a user who modifies this file could inject arbitrary paths that would be used for glob scanning in `_scan_artifact_existence`.
- **Impact:** A user with write access to `.a0proj/instructions/01-bmad-config.md` could redirect artifact scanning to arbitrary directories. The results are only used for phase completion checks (boolean), not exposed externally.
- **Recommendation:** Validate resolved paths are within the expected project root:
  ```python
  resolved = Path(resolved_path).resolve()
  if not str(resolved).startswith(str(project_root)):
      continue  # Skip paths outside project
  ```

---

### [INFO] Test/Example Credentials in TEA Knowledge Documentation

- **Location:** `skills/bmad-tea/testarch/knowledge/*.md` (multiple files)
- **Description:** The TEA knowledge base files contain example credentials (`SecurePass123!`, `password`, `test@example.com`) and API token patterns. These are instructional examples for test architecture patterns, not real credentials.
- **Impact:** None in production. These are documentation files teaching testing patterns.
- **Recommendation:** No action required. The examples are clearly instructional. Consider adding a comment at the top of each file: `<!-- Example code for instructional purposes only -->`

---

### [INFO] PyYAML 6.0.3 — No Known Vulnerabilities

- **Location:** Project dependency
- **Description:** PyYAML version 6.0.3 is the latest stable release with no known CVEs. The routing extension correctly uses `yaml.safe_load()` which prevents arbitrary code execution via YAML deserialization.
- **Impact:** None.
- **Recommendation:** No action required. Continue using `yaml.safe_load()` and pin the dependency version.

---

### [INFO] Shell Scripts Use Safe Defaults

- **Location:** All shell scripts in the plugin
- **Description:** All four shell scripts (`bmad-init.sh`, `promote.sh`, `import-sidecars.sh`, `bmad-state-write.sh`) use `set -euo pipefail`, properly quote variables, and avoid `eval`. The `promote.sh` script explicitly validates the `NAME` argument against path traversal (`/`, `..`, `^-`).
- **Impact:** None. This is a positive observation.
- **Recommendation:** No action required.

---

### [INFO] Dashboard Uses XSS-Safe Rendering

- **Location:** `webui/bmad-dashboard.html` and `webui/bmad-dashboard-store.js`
- **Description:** The BMAD dashboard uses Alpine.js `x-text` directives for all dynamic content rendering. `x-text` sets `textContent` (not `innerHTML`), which is inherently safe against XSS. No `v-html` or `innerHTML` usage was found in the dashboard.
- **Impact:** None. This is a positive observation.
- **Recommendation:** No action required.

---

## Positive Observations

1. **YAML parsing is safe** — `yaml.safe_load()` used exclusively; no `yaml.load()` anywhere in the codebase
2. **Path traversal protection** — `promote.sh` validates NAME against `/`, `..`, and `^-` prefixes
3. **Shell safety** — All scripts use `set -euo pipefail` and properly quote variables
4. **No hardcoded secrets** — No real API keys, tokens, or passwords found in production code
5. **XSS-safe dashboard** — Alpine.js `x-text` prevents XSS in the status dashboard
6. **Graceful error handling** — Routing extension wraps all operations in try/except with logging, never crashes the agent loop
7. **Safe TOML parsing** — `resolve_customization.py` uses stdlib `tomllib` (no code execution risk)
8. **Proper `.gitignore`** — Excludes `.a0proj/`, agent settings, IDE directories, and sensitive state
9. **No `eval()` usage** — Zero instances of `eval()` in any Python or JavaScript file
10. **Dependency hygiene** — Only PyYAML as an external dependency; stdlib `tomllib` used for TOML
11. **Profile gating** — Routing extension only runs for `bmad-master` profile, reducing attack surface
12. **Cache invalidation** — mtime-based cache keys ensure stale data is never served

---

## Recommendations

### Priority 1 — Fix Before Next Release

1. **Sanitize `DATA.grade` in BMB report generators** — Add allowlist validation for grade values to prevent CSS class injection (HIGH)
2. **Replace `shell=True` with `os.startfile()`** on Windows — Remove the shell injection vector (MEDIUM)

### Priority 2 — Fix in Current Sprint

3. **Sanitize API error responses** — Return generic errors to clients, log details server-side (MEDIUM)
4. **Validate glob patterns** from YAML `outputs` field — Prevent recursive/traversal patterns (MEDIUM)

### Priority 3 — Defense in Depth

5. **Add size limits** to YAML cache entries — Prevent memory exhaustion from oversized files (LOW)
6. **Validate alias paths** stay within project root — Prevent path redirection in config (LOW)
7. **Document `esc()` requirement** for BMB report generators — Reduce future XSS risk (LOW)

---

## Audit Coverage Matrix

| Dimension | Files Checked | Issues Found |
|-----------|--------------|-------------|
| Input Handling | routing extension, customization resolver | Glob pattern injection (MED) |
| Authentication & Authorization | API endpoint, routing profile gate | None |
| Data Protection | Secrets scan, .gitignore, error messages | Info disclosure in API (MED) |
| Infrastructure | Dependencies, shell scripts, file permissions | shell=True (MED), cache size (LOW) |
| Third-Party Integrations | PyYAML, Alpine.js dashboard | CSS class injection (HIGH), innerHTML pattern (LOW) |

---

*Report generated by Agent Zero Security Auditor. OWASP Top 10 used as minimum baseline.*
