# Language

Shared architecture vocabulary for `tdd` and `improve-codebase-architecture`. Use these exact terms — never "component," "service," "API," or (in architecture talk) "boundary." Consistency is the point: a precise shared language costs fewer tokens than re-explaining concepts.

## Terms

**Module** — anything with an interface and an implementation. Scale-agnostic: function, class, package, or tier-spanning slice. _Not_: unit, component, service.

**Interface** — everything a caller must know to use the module correctly: the type signature plus invariants, ordering constraints, error modes, required config, performance traits. _Not_: API, signature — those name only the type-level surface.

**Implementation** — the code inside a module. Say "adapter" when the seam is the topic, "implementation" otherwise. A small adapter can hide a large implementation (a Postgres repo); a large adapter can hide a small one (an in-memory fake).

**Depth** — behaviour per unit of interface a caller must learn. **Deep** = much behaviour behind a small interface. **Shallow** = interface nearly as complex as what it hides.

**Seam** _(Feathers)_ — a place where behaviour can change without editing in place; where a module's interface lives. Placing the seam is its own design decision, separate from what goes behind it. _Not_: "boundary" — collides with DDD's bounded context. Exception: "system boundary" in the AGENTS.md testing sense (network, clock, filesystem, env) is established usage; keep it there.

**Adapter** — a concrete thing satisfying an interface at a seam. Names the role, not the contents.

**Leverage** — the caller's win from depth: one implementation pays back across N call sites and M tests.

**Locality** — the maintainer's win from depth: change, bugs, knowledge, and verification concentrate in one place. Fix once, fixed everywhere.

## Principles

- **Depth lives at the interface, not the implementation.** A deep module may be built from small swappable parts internally — they're just not part of the interface. Internal seams (private, used by the module's own tests) can coexist with the external seam.
- **Deletion test.** Delete the module in your head. Complexity vanishes → it was a pass-through. Complexity reappears across N callers → it was earning its keep.
- **The interface is the test surface.** Tests and callers cross the same seam. Needing to test past it means the module is the wrong shape.
- **One adapter = hypothetical seam. Two = real.** Don't cut a seam until something actually varies across it.

## Rejected framings

- Depth as implementation-lines over interface-lines (Ousterhout's ratio): rewards padding the implementation. Use depth-as-leverage.
- Interface as `Protocol` / ABC / public method list: too narrow — the interface is every fact a caller needs, not just the typed surface.
