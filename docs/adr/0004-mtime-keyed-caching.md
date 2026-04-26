# ADR-0004: mtime-Keyed Caching for File Reads

**Status:** Accepted
**Date:** 2026-04-26
**Phase:** B (Structural Alignment)

## Context

The routing extension and API module read CSV files and alias mappings frequently (every message loop iteration). The original cache used path strings as keys without invalidation — file changes within the same process were invisible.

## Decision

Use composite cache keys of `(path_str, mtime_ns)` with bounded FIFO eviction (max 128 entries).

## Rationale

- `os.stat().st_mtime_ns` provides nanosecond-precision modification time
- Composite key naturally invalidates when file changes (new mtime = new key)
- Bounded eviction prevents unbounded memory growth
- FIFO eviction is simple and sufficient (no LRU complexity needed)
- A0 extensions are synchronous — no race conditions on cache access

## Consequences

- **Positive:** Cache always reflects current file state
- **Positive:** No manual cache invalidation needed
- **Positive:** Memory bounded to 128 entries max
- **Negative:** Extra `os.stat()` call per cache miss (negligible cost)
- **Negative:** Stale entries accumulate until eviction threshold (mitigated by 128 limit)

## Alternatives Considered

1. **Path-only keys with TTL** — adds timer complexity, still serves stale data within TTL
2. **Unbounded cache** — memory leak risk for long-running sessions
3. **No caching** — re-reads CSV from disk every message (I/O waste)
