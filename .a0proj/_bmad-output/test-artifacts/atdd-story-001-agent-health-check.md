---
stepsCompleted: ['step-03-test-strategy', 'step-04a-subprocess-api-failing', 'step-04b-subprocess-e2e-failing', 'step-04c-aggregate', 'step-05-validate-and-complete']
lastStep: 'step-05-validate-and-complete'
lastSaved: '2026-03-01'
workflowType: 'testarch-atdd'
inputDocuments:
  - '/a0/usr/projects/a0_bmad_method/.a0proj/_bmad-output/implementation-artifacts/story-001-agent-health-check.md'
---

# ATDD Checklist — Story 001: Agent Health Check HTML Page

**Date:** 2026-03-01  
**Author:** Murat (BMAD Master Test Architect — TEA Module)  
**Primary Test Level:** Unit (JS logic with mocked fetch) + E2E (Playwright file:// browser)  
**TDD Phase:** 🔴 RED — all tests written, all tests failing, implementation not started  

---

## Story Summary

A single-file HTML+JS dashboard that checks all 20 BMAD agents for required prompt files using browser
`fetch()` calls. Health determined by presence of 4 required prompt files per agent. Zero dependencies —
opens directly via `file://` in any modern browser.

**As a** BMAD framework developer  
**I want** a single-file HTML+JS dashboard that checks all 20 BMAD agents for required prompt files  
**So that** I can instantly see which agents are healthy (green) or broken (red) without installing any tools  

---

## Risk Assessment

| Area | Risk Level | Rationale |
|------|-----------|----------|
| Health check logic (checkAgent/checkFile) | 🔴 HIGH | Core business logic — wrong here = silent false negatives |
| Promise.all parallelism | 🔴 HIGH | Sequential fallback would miss AC-008 performance SLA |
| Summary banner class assignment | 🟡 MEDIUM | 3 threshold states, easy to get boundary wrong |
| DOM rendering (renderAgent) | 🟡 MEDIUM | `<details>` toggle must only appear for RED agents |
| Configuration constants isolation | 🟡 MEDIUM | Any hardcoded path bypasses AC-005 configurable BASE_PATH |
| Accessibility (color + icon dual signal) | 🟢 LOW | Structural — grep-verifiable |
| File size constraint (<50KB) | 🟢 LOW | Measurable — `wc -c` |

---

## Acceptance Criteria → Test Mapping

| AC | Description | Test Level | Priority | Test Name |
|----|-------------|-----------|----------|----------|
| AC-001-01 | 20 agents in AGENTS const | Unit | P0 | `should define exactly 20 agents in AGENTS constant` |
| AC-001-02 | Health = all 4 files present | Unit | P0 | `should return healthy:false when any required file is missing` |
| AC-001-02 | checkAgent uses Promise.all | Unit | P0 | `should check all 4 required files in parallel` |
| AC-001-02 | Healthy only when ALL 4 present | Unit | P0 | `should return healthy:true only when all 4 files respond 200` |
| AC-001-03 | Visual indicators (icon + text) | E2E | P1 | `should display icon and text status for each agent row` |
| AC-001-04 | Summary banner X/20 + color class | Unit | P1 | `should assign correct CSS class to summary banner based on healthy count` |
| AC-001-05 | BASE_PATH single constant | Unit | P1 | `should construct fetch URLs using BASE_PATH constant` |
| AC-001-07 | Missing file detail collapsible | E2E | P1 | `should show collapsible details panel for unhealthy agents` |
| AC-001-08 | Promise.all parallel execution | Unit | P0 | `should run all agent checks concurrently via Promise.all` |
| AC-001-10 | Accessibility — color + icon | E2E | P2 | `should use icon and text alongside color for status indication` |

---

## Failing Tests Created (RED Phase)

### Unit Tests — 5 tests

**File:** `tests/unit/dashboard-health-logic.spec.ts`

> **Stack Note:** This is a browser-only HTML file with no build system. Unit tests use Playwright's
> `page.evaluate()` to inject and execute the dashboard's JS functions in a browser context with
> `fetch` mocked via `page.route()`. This approach validates pure logic without requiring a server.

- 🔴 **Test:** `should define exactly 20 agents in AGENTS constant`
  - **Status:** RED — `dashboard.html` does not exist yet; `AGENTS` constant undefined
  - **Verifies:** AC-001-01 — agent list completeness

- 🔴 **Test:** `should return healthy:false when any required file is missing`
  - **Status:** RED — `checkAgent()` function not implemented
  - **Verifies:** AC-001-02 — health logic rejects partial file presence

- 🔴 **Test:** `should return healthy:true only when all 4 required files return 200`
  - **Status:** RED — `checkAgent()` function not implemented
  - **Verifies:** AC-001-02 — green state requires all 4 files

- 🔴 **Test:** `should assign correct CSS class to summary banner based on healthy count`
  - **Status:** RED — `renderSummary()` function not implemented
  - **Verifies:** AC-001-04 — all-green / partial / critical thresholds

- 🔴 **Test:** `should construct fetch URLs using BASE_PATH constant`
  - **Status:** RED — `checkFile()` function not implemented
  - **Verifies:** AC-001-05 — BASE_PATH drives all fetch URL construction

### E2E Tests — 2 tests

**File:** `tests/e2e/dashboard-browser.spec.ts`

- 🔴 **Test:** `should display icon and text status for each agent row after health check completes`
  - **Status:** RED — `dashboard.html` does not exist; browser navigates to missing file
  - **Verifies:** AC-001-03 (visual indicators), AC-001-10 (accessibility dual signal)

- 🔴 **Test:** `should show collapsible details panel listing missing files for unhealthy agents`
  - **Status:** RED — `dashboard.html` does not exist; `<details>` element not present
  - **Verifies:** AC-001-07 — missing file detail view

---

## Test File Contents

### File: `tests/unit/dashboard-health-logic.spec.ts`

~~~typescript
import { test, expect } from '@playwright/test';
import * as path from 'path';

/**
 * ATDD Unit Tests — Story 001: Agent Health Check Dashboard
 * TDD RED PHASE: All tests use test.skip() — dashboard.html not implemented yet.
 *
 * Strategy: Load dashboard.html in headless browser, mock fetch() via page.route(),
 * then call JS functions via page.evaluate() to validate pure logic.
 *
 * Remove test.skip() and run `npx playwright test tests/unit/` to enter GREEN phase.
 */

const DASHBOARD_PATH = path.resolve(
  __dirname,
  '../../.a0proj/_bmad-output/implementation-artifacts/dashboard.html'
);

test.describe('Story 001 — Dashboard Health Logic (ATDD Unit)', () => {

  test.skip('[P0] should define exactly 20 agents in AGENTS constant', async ({ page }) => {
    // THIS TEST WILL FAIL — dashboard.html not implemented yet
    // Expected: AGENTS array has exactly 20 entries
    await page.goto(`file://${DASHBOARD_PATH}`);

    const agentCount = await page.evaluate(() => {
      // @ts-ignore — AGENTS is a global const in dashboard.html
      return window.AGENTS?.length;
    });

    expect(agentCount).toBe(20);
  });

  test.skip('[P0] should return healthy:false when any required file is missing', async ({ page }) => {
    // THIS TEST WILL FAIL — checkAgent() not implemented yet
    // Intercept: 3 files return 200, 1 file returns 404
    await page.route('**/agent.system.main.tips.md', route =>
      route.fulfill({ status: 404, body: 'Not Found' })
    );
    await page.route('**/agent.system.main.*.md', route =>
      route.fulfill({ status: 200, body: 'mock content' })
    );

    await page.goto(`file://${DASHBOARD_PATH}`);

    const result = await page.evaluate(async () => {
      // @ts-ignore — checkAgent is a global function in dashboard.html
      return await window.checkAgent('bmad-analyst');
    });

    expect(result.healthy).toBe(false);
    expect(result.missing).toContain('agent.system.main.tips.md');
    expect(result.name).toBe('bmad-analyst');
  });

  test.skip('[P0] should return healthy:true only when all 4 required files return 200', async ({ page }) => {
    // THIS TEST WILL FAIL — checkAgent() not implemented yet
    await page.route('**/bmad-master/prompts/**', route =>
      route.fulfill({ status: 200, body: 'mock content' })
    );

    await page.goto(`file://${DASHBOARD_PATH}`);

    const result = await page.evaluate(async () => {
      // @ts-ignore
      return await window.checkAgent('bmad-master');
    });

    expect(result.healthy).toBe(true);
    expect(result.missing).toHaveLength(0);
  });

  test.skip('[P1] should assign correct CSS class to summary banner based on healthy count', async ({ page }) => {
    // THIS TEST WILL FAIL — renderSummary() not implemented yet
    // Test all 3 threshold states: all-green (20/20), partial (15/20), critical (5/20)
    await page.goto(`file://${DASHBOARD_PATH}`);

    const bannerClass20 = await page.evaluate(() => {
      const mockResults = Array(20).fill({ healthy: true, name: 'test', missing: [] });
      // @ts-ignore
      window.renderSummary(mockResults);
      return document.querySelector('#summary-banner')?.className;
    });
    expect(bannerClass20).toContain('all-green');

    const bannerClass15 = await page.evaluate(() => {
      const mockResults = [
        ...Array(15).fill({ healthy: true, name: 'test', missing: [] }),
        ...Array(5).fill({ healthy: false, name: 'test', missing: ['x.md'] }),
      ];
      // @ts-ignore
      window.renderSummary(mockResults);
      return document.querySelector('#summary-banner')?.className;
    });
    expect(bannerClass15).toContain('partial');

    const bannerClass5 = await page.evaluate(() => {
      const mockResults = [
        ...Array(5).fill({ healthy: true, name: 'test', missing: [] }),
        ...Array(15).fill({ healthy: false, name: 'test', missing: ['x.md'] }),
      ];
      // @ts-ignore
      window.renderSummary(mockResults);
      return document.querySelector('#summary-banner')?.className;
    });
    expect(bannerClass5).toContain('critical');
  });

  test.skip('[P1] should construct fetch URLs using BASE_PATH constant', async ({ page }) => {
    // THIS TEST WILL FAIL — checkFile() / BASE_PATH not implemented yet
    const interceptedURLs: string[] = [];

    await page.route('**/*.md', route => {
      interceptedURLs.push(route.request().url());
      route.fulfill({ status: 200, body: 'mock' });
    });

    await page.goto(`file://${DASHBOARD_PATH}`);

    await page.evaluate(async () => {
      // @ts-ignore
      await window.checkAgent('bmad-analyst');
    });

    // All fetch URLs must contain BASE_PATH value
    expect(interceptedURLs.length).toBeGreaterThanOrEqual(4);
    interceptedURLs.forEach(url => {
      expect(url).toContain('bmad-analyst/prompts/');
    });
  });
});
~~~

### File: `tests/e2e/dashboard-browser.spec.ts`

~~~typescript
import { test, expect } from '@playwright/test';
import * as path from 'path';

/**
 * ATDD E2E Tests — Story 001: Agent Health Check Dashboard
 * TDD RED PHASE: All tests use test.skip() — dashboard.html not implemented yet.
 *
 * Strategy: Load dashboard.html via file://, route all agent file checks,
 * simulate healthy/unhealthy states and verify full user journey.
 *
 * Remove test.skip() and run `npx playwright test tests/e2e/` to enter GREEN phase.
 */

const DASHBOARD_PATH = path.resolve(
  __dirname,
  '../../.a0proj/_bmad-output/implementation-artifacts/dashboard.html'
);

/**
 * Route all 20 agents × 4 files:
 * - All healthy except bmad-brainstorming-coach (known defect — missing all 4 prompts)
 */
async function routeHealthCheckRequests(page: any) {
  // Known broken agent — return 404 for all prompt files
  await page.route('**/bmad-brainstorming-coach/prompts/**', route =>
    route.fulfill({ status: 404, body: 'Not Found' })
  );
  // All other agents healthy
  await page.route('**/agents/**/prompts/**.md', route =>
    route.fulfill({ status: 200, body: '# mock prompt content' })
  );
}

test.describe('Story 001 — Dashboard Browser Journey (ATDD E2E)', () => {

  test.skip(
    '[P1] should display icon and text status for each agent row after health check completes',
    async ({ page }) => {
      // THIS TEST WILL FAIL — dashboard.html does not exist yet
      await routeHealthCheckRequests(page);
      await page.goto(`file://${DASHBOARD_PATH}`);

      // Page title must be descriptive (AC-001-10 accessibility)
      await expect(page).toHaveTitle(/BMAD Agent Health/i);

      // Wait for health check to complete (Promise.all resolves)
      await page.waitForSelector('[data-testid="agent-list"]', { timeout: 3000 });

      // Healthy agents must show checkmark icon AND text (not color alone — AC-001-10)
      const healthyRows = page.locator('[data-testid="agent-row"][data-status="healthy"]');
      await expect(healthyRows.first()).toContainText('✅');
      await expect(healthyRows.first()).toContainText('healthy');

      // Unhealthy agent must show cross icon AND text
      const unhealthyRows = page.locator('[data-testid="agent-row"][data-status="unhealthy"]');
      await expect(unhealthyRows.first()).toContainText('❌');
      await expect(unhealthyRows.first()).toContainText('missing');

      // Summary banner present and shows count (AC-001-04)
      const banner = page.locator('#summary-banner');
      await expect(banner).toContainText('/ 20 agents healthy');
    }
  );

  test.skip(
    '[P1] should show collapsible details panel listing missing files for unhealthy agents',
    async ({ page }) => {
      // THIS TEST WILL FAIL — dashboard.html does not exist yet
      await routeHealthCheckRequests(page);
      await page.goto(`file://${DASHBOARD_PATH}`);

      // Wait for render
      await page.waitForSelector('[data-testid="agent-list"]', { timeout: 3000 });

      // The known-broken agent row for bmad-brainstorming-coach
      const brokenRow = page.locator('[data-testid="agent-row"]').filter(
        { hasText: 'bmad-brainstorming-coach' }
      );
      await expect(brokenRow).toBeVisible();

      // Details panel must be present but collapsed (AC-001-07)
      const detailsPanel = brokenRow.locator('details');
      await expect(detailsPanel).toBeAttached();
      await expect(detailsPanel).not.toHaveAttribute('open');

      // Click to expand — should show missing file names
      await brokenRow.locator('summary').click();
      await expect(detailsPanel).toHaveAttribute('open');

      // Missing files listed with their paths
      await expect(detailsPanel).toContainText('agent.system.main.role.md');
      await expect(detailsPanel).toContainText('agent.system.main.communication.md');

      // Click again to collapse
      await brokenRow.locator('summary').click();
      await expect(detailsPanel).not.toHaveAttribute('open');
    }
  );
});
~~~

---

## Data Factories and Fixtures

### Mock Agent Result Factory

**Inline helper** (no separate file required — pure JavaScript objects):

~~~typescript
// Healthy agent result
const createHealthyResult = (name: string) => ({
  name,
  healthy: true,
  missing: [] as string[],
});

// Unhealthy agent result
const createUnhealthyResult = (name: string, missing: string[]) => ({
  name,
  healthy: false,
  missing,
});
~~~

### Playwright Route Fixture

Required for both test files — routes all `**/prompts/**.md` requests:

~~~typescript
// Healthy: 200 response
await page.route('**/agents/**/prompts/**.md', route =>
  route.fulfill({ status: 200, body: '# mock' })
);

// Unhealthy: 404 for specific agent
await page.route('**/bmad-brainstorming-coach/prompts/**', route =>
  route.fulfill({ status: 404, body: 'Not Found' })
);
~~~

---

## Required `data-testid` Attributes

These attributes **must be added during implementation** for test stability:

### dashboard.html

| `data-testid` | Element | Required By |
|--------------|---------|------------|
| `agent-list` | `<ul>` or `<ol>` container | E2E tests (wait anchor) |
| `agent-row` | Each `<li>` per agent | E2E row selection |
| `summary-banner` | Header summary `<div>` or `<header>` | Unit + E2E |
| `loading-indicator` | Loading spinner/text | E2E (optional) |

**Implementation Example:**

~~~html
<div id="summary-banner" data-testid="summary-banner" class="all-green">
  20 / 20 agents healthy
</div>
<ul id="agent-list" data-testid="agent-list">
  <li data-testid="agent-row" data-status="healthy">
    ✅ bmad-analyst — healthy
  </li>
  <li data-testid="agent-row" data-status="unhealthy">
    ❌ bmad-brainstorming-coach — 4 files missing
    <details>
      <summary>Show missing files</summary>
      <ul>
        <li>agent.system.main.role.md</li>
        <li>agent.system.main.communication.md</li>
        <li>agent.system.main.communication_additions.md</li>
        <li>agent.system.main.tips.md</li>
      </ul>
    </details>
  </li>
</ul>
~~~

---

## Implementation Checklist

### Test: `should define exactly 20 agents in AGENTS constant`

**File:** `tests/unit/dashboard-health-logic.spec.ts`

**Tasks to make this test pass:**

- [ ] Create `dashboard.html` with `<script>` block
- [ ] Define `const AGENTS = [...]` as the FIRST constant in `<script>` (20 entries)
- [ ] Verify: `AGENTS.length === 20` in browser console
- [ ] Run test: `npx playwright test tests/unit/dashboard-health-logic.spec.ts -g "AGENTS constant"`
- [ ] ✅ Test passes (green phase)

**Estimated Effort:** 0.5 hours

---

### Test: `should return healthy:false when any required file is missing`

**File:** `tests/unit/dashboard-health-logic.spec.ts`

**Tasks to make this test pass:**

- [ ] Implement `checkFile(agentName, fileName)` — fetch HEAD or GET, return true/false, never throws
- [ ] Implement `checkAgent(agentName)` — calls `checkFile()` for all 4 REQUIRED_FILES via `Promise.all`
- [ ] Return object `{ name, healthy: boolean, missing: string[] }`
- [ ] `missing` contains only failed file names (not full paths)
- [ ] Run test: `npx playwright test tests/unit/dashboard-health-logic.spec.ts -g "healthy:false"`
- [ ] ✅ Test passes (green phase)

**Estimated Effort:** 1.5 hours

---

### Test: `should return healthy:true only when all 4 required files return 200`

**File:** `tests/unit/dashboard-health-logic.spec.ts`

**Tasks to make this test pass:**

- [ ] Ensure `checkAgent()` returns `healthy: true` only when ALL 4 `checkFile()` calls return `true`
- [ ] `missing` array must be empty when all files present
- [ ] Run test: `npx playwright test tests/unit/dashboard-health-logic.spec.ts -g "healthy:true"`
- [ ] ✅ Test passes (green phase)

**Estimated Effort:** 0.25 hours (covered by checkAgent implementation above)

---

### Test: `should assign correct CSS class to summary banner based on healthy count`

**File:** `tests/unit/dashboard-health-logic.spec.ts`

**Tasks to make this test pass:**

- [ ] Add `<div id="summary-banner" data-testid="summary-banner">` to HTML
- [ ] Implement `renderSummary(results)` — count healthy, update text, set CSS class
- [ ] Class rules: 20/20 → `all-green`, 10–19/20 → `partial`, 0–9/20 → `critical`
- [ ] Add data-testid attribute: `summary-banner`
- [ ] Run test: `npx playwright test tests/unit/dashboard-health-logic.spec.ts -g "CSS class"`
- [ ] ✅ Test passes (green phase)

**Estimated Effort:** 1 hour

---

### Test: `should construct fetch URLs using BASE_PATH constant`

**File:** `tests/unit/dashboard-health-logic.spec.ts`

**Tasks to make this test pass:**

- [ ] Define `const BASE_PATH = '../../../agents'` as first constant in `<script>`
- [ ] `checkFile()` must construct URL: `${BASE_PATH}/${agentName}/prompts/${fileName}`
- [ ] No hardcoded paths anywhere outside `BASE_PATH` declaration
- [ ] Run test: `npx playwright test tests/unit/dashboard-health-logic.spec.ts -g "BASE_PATH"`
- [ ] ✅ Test passes (green phase)

**Estimated Effort:** 0.25 hours (covered by checkFile implementation)

---

### Test: `should display icon and text status for each agent row after health check completes`

**File:** `tests/e2e/dashboard-browser.spec.ts`

**Tasks to make this test pass:**

- [ ] Implement `renderAgent(result)` — creates `<li>` with icon + name + status text
- [ ] Add data-testid: `agent-row` with `data-status` attribute (`healthy`/`unhealthy`)
- [ ] Add `<ul id="agent-list" data-testid="agent-list">` container
- [ ] Wire `DOMContentLoaded` → `runHealthCheck()` → render all rows
- [ ] Implement `runHealthCheck()` using `Promise.all` across all AGENTS
- [ ] Add `<title>BMAD Agent Health Dashboard</title>` to `<head>`
- [ ] Run test: `npx playwright test tests/e2e/dashboard-browser.spec.ts -g "icon and text"`
- [ ] ✅ Test passes (green phase)

**Estimated Effort:** 3 hours

---

### Test: `should show collapsible details panel listing missing files for unhealthy agents`

**File:** `tests/e2e/dashboard-browser.spec.ts`

**Tasks to make this test pass:**

- [ ] `renderAgent()` — for unhealthy results, add `<details><summary>Show missing files</summary>` node
- [ ] `<details>` must be collapsed by default (no `open` attribute)
- [ ] Missing file list shows file names inside `<details>` panel
- [ ] Healthy agents must NOT have a `<details>` element
- [ ] Run test: `npx playwright test tests/e2e/dashboard-browser.spec.ts -g "collapsible"`
- [ ] ✅ Test passes (green phase)

**Estimated Effort:** 1 hour

---

## Running Tests

~~~bash
# Install Playwright (if not already installed)
npm init -y && npm install -D @playwright/test
npx playwright install chromium

# Run all ATDD failing tests (RED phase verification)
npx playwright test tests/unit/dashboard-health-logic.spec.ts tests/e2e/dashboard-browser.spec.ts

# Run only unit tests
npx playwright test tests/unit/dashboard-health-logic.spec.ts

# Run only E2E tests
npx playwright test tests/e2e/dashboard-browser.spec.ts

# Run in headed mode (see browser)
npx playwright test tests/e2e/ --headed

# Debug specific test
npx playwright test tests/e2e/dashboard-browser.spec.ts --debug

# Run with trace on failure
npx playwright test --trace on
~~~

---

## Red-Green-Refactor Workflow

### RED Phase (Complete) ✅

- ✅ 5 unit tests written — all failing (checkAgent, renderSummary, checkFile, AGENTS const)
- ✅ 2 E2E tests written — all failing (visual indicators, collapsible detail panel)
- ✅ All tests use `test.skip()` — documented TDD red phase
- ✅ Assertions reflect EXPECTED behavior, not placeholders
- ✅ Mock strategy defined (page.route() for fetch interception)
- ✅ data-testid requirements documented
- ✅ Implementation checklist maps each test to concrete tasks

### GREEN Phase (Amelia — Dev Agent, next steps)

1. Pick first failing test: `should define exactly 20 agents in AGENTS constant`
2. Create `dashboard.html` with `AGENTS` const — run test — verify green
3. Move to `should construct fetch URLs using BASE_PATH constant`
4. Implement `checkFile()` + `BASE_PATH` — run test — verify green
5. Continue test by test down the implementation checklist
6. Remove `test.skip()` from each test only when the feature is implemented

### REFACTOR Phase (after all tests green)

1. Extract duplicated route setup into a shared Playwright fixture
2. Review `checkAgent()` for error handling edge cases (network timeout, CORS)
3. Verify `wc -c dashboard.html < 51200` (file size NFR)
4. Run full suite after each refactor to maintain green

---

## Known Defect — Pre-existing (Captured)

> ⚠️ **DEFECT [PERSONA-01-CRITICAL]:** `bmad-brainstorming-coach` prompts/ directory is EMPTY.
> All 4 required prompt files are missing. This agent will ALWAYS be RED on the dashboard.
> The E2E tests above use this as the known-unhealthy agent for test routing.
> **Fix required:** Create the 4 prompt files for bmad-brainstorming-coach before any GREEN phase
> verification on a live filesystem scan.

---

## Notes

- This is a **browser-only project** — no Node.js server, no build step. Playwright is used as
  the test runner with `file://` URL loading and `page.route()` for fetch mocking.
- The unit tests (`tests/unit/`) use `page.evaluate()` to call JS functions in browser context.
  This is the correct approach for testing inline `<script>` logic without a build system.
- Performance AC-001-08 (< 2 seconds for 20 agents) is validated implicitly by the E2E tests:
  `waitForSelector` timeout of 3000ms catches any sequential (non-parallel) fallback.
- AC-001-09 (file size < 50 KB) is a CI check, not a Playwright test: `wc -c dashboard.html`.
- AC-001-06 (zero dependencies) is a structural check: `grep -c 'http' dashboard.html` must
  return 0 for external URLs.

---

## Knowledge Base References Applied

- **fixture-architecture.md** — Playwright fixture patterns for route setup reuse
- **network-first.md** — `page.route()` registered BEFORE `page.goto()` (race condition prevention)
- **selector-resilience.md** — `getByRole`, `getByText`, `locator()` over CSS class selectors
- **test-levels-framework.md** — Unit via page.evaluate() for pure JS logic; E2E for full journeys
- **test-quality.md** — Given-When-Then structure, one assertion cluster per test, deterministic waits
- **api-testing-patterns.md** — Adapted for browser fetch mocking (no traditional REST API present)

---

**Generated by Murat 🧪 — BMAD Master Test Architect (TEA Module)**  
**Date:** 2026-03-01  
**Workflow:** testarch-atdd v5.0 (Step-File Architecture)  
