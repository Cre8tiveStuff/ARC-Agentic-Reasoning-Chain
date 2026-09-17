# ARC - Agentic Reasoning Chain

**Open towards Team Collaborations & Contract Opportunities.**

Reusable infrastructure for multi-step agent tool-calling - extracted from real patterns built O2A, generalized so any future agent project can use them without rebuilding the same safety and observability logic from scratch.

## What lives here

ARC is not a standalone application.  It's a small, focused utility layer that other agents projects (like O2A) depend on.

## Status

| Component | Purpose | Status |
|---|---|---|
| `@idempotent` decorator | Wraps any function with hash-based duplicate-call prevention and processing lock | Not started |
| Chain-correlation logger | Tags multiple related tool calls with a shared run ID for observability | Not started |
| Chain-testing helper | Asserts an agent called tools in a specific order, for tests | Not started |

## Origin

The idempotency/locking pattern was first built directly inside procurement-rag's `refresh_index()` tool. This repo extracts that pattern into something reusable, rather than duplicating it in every future project that needs the same safety guarantee.
 
