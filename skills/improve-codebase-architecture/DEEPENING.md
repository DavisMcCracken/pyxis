# Deepening

How to deepen a cluster of shallow modules safely, by dependency category. Vocabulary: [../_shared/LANGUAGE.md](../_shared/LANGUAGE.md).

## Dependency categories

Classify each dependency of the candidate; the category dictates how the deepened module is tested across its seam.

### 1. In-process

Pure computation, in-memory state, no I/O. Always deepenable: merge the modules, test directly through the new interface. No adapter.

### 2. Local-substitutable

Has a local test stand-in — SQLite `:memory:` for the DB layer, `tmp_path` for the filesystem, an injected clock for time. Deepenable when the stand-in exists; tests run against it inside the suite. The seam stays internal — no port in the external interface.

### 3. Remote but owned — ports & adapters

Your own services across a network seam (internal APIs, microservices). Cut a **port** (in Python, a `Protocol`) at the seam; the deep module owns the logic, transport arrives as an injected **adapter**. Tests use an in-memory adapter; production uses HTTP/gRPC/queue.

Recommendation shape: *"Port at the seam; HTTP adapter for production, in-memory adapter for tests — the logic stays in one deep module even though deployment crosses a network."*

### 4. True external — fake

Third-party services you don't control (Stripe, Twilio). Injected port again; tests provide a hand-written fake adapter (preference order in the `tdd` skill's tests.md — fake before `MagicMock`).

## Seam discipline

- **Two adapters or no port.** Production + test is the usual pair. A single-adapter seam is indirection, not architecture.
- **Internal vs external seams.** A deep module may keep private internal seams for its own tests. Don't promote them into the interface because tests happen to use them.

## Testing strategy: replace, don't layer

- Interface-level tests make the old unit tests on absorbed shallow modules waste — delete them.
- New tests live at the deepened interface; assert observable outcomes, never internal state.
- A test that must change when the implementation changes was testing past the interface.
