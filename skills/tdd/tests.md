# Good Tests, Bad Tests, and Faking

Python companion to [SKILL.md](SKILL.md). Matches the AGENTS.md Testing rules — this file is the long form.

## Good tests

Integration-style: real interfaces, real code paths.

```python
def test_checkout_with_valid_cart(cart: Cart) -> None:
    cart.add(PRODUCT)
    result = checkout(cart, payment_method=TEST_CARD)
    assert result.status is Status.CONFIRMED
```

Characteristics:

- Tests behavior callers care about, through the public API only
- Survives internal refactors
- Name says WHAT, not HOW
- One logical assertion per test

Verify through the interface, not around it:

```python
# BAD: bypasses the interface to verify
def test_create_user_saves_row(db: Connection) -> None:
    create_user(name="Alice")
    row = db.execute("SELECT * FROM users WHERE name = ?", ("Alice",)).fetchone()
    assert row is not None

# GOOD: verifies through the interface
def test_created_user_is_retrievable() -> None:
    user = create_user(name="Alice")
    assert get_user(user.id).name == "Alice"
```

## Bad tests

Red flags:

- Mocking internal collaborators (`mocker.patch("myapp.orders._calculate_total")`)
- Testing private functions directly
- Asserting on call counts or call order (`assert mock.call_count == 2`)
- Test breaks on refactor without behavior change
- Test name describes implementation ("calls payment service") instead of behavior ("charges the customer once")

```python
# BAD: tests that internals were called, not that behavior happened
def test_checkout_calls_payment_service(mocker) -> None:
    mock = mocker.patch("myapp.checkout.payment_service.process")
    checkout(cart, payment)
    mock.assert_called_once_with(cart.total)
```

## Faking — where and how

Fake only at system boundaries: **network, clock, filesystem, env** (the AGENTS.md rule). Never mock your own modules, internal collaborators, or the unit under test.

Preference order:

1. **Real thing with test-controlled state** — `tmp_path` for filesystem, SQLite `:memory:` for a DB layer.
2. **Hand-written fake** — a small class implementing the seam. Readable, typed, reusable:

```python
class FakeClock:
    """Hand-written fake for the time boundary."""

    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


def test_entry_expires(clock: FakeClock) -> None:
    cache = TTLCache(clock=clock)
    cache.set("a", 1, ttl=10)
    clock.advance(10)
    assert cache.get("a") is None
```

3. **`monkeypatch`** — for env vars, attributes you don't control:

```python
def test_reads_token_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_TOKEN", "test-token")
    assert load_config().token == "test-token"
```

4. **`unittest.mock.MagicMock`** — last resort, third-party interfaces too wide to fake by hand.

## Designing for fakeability

**Accept dependencies, don't create them.** The dependency is part of the interface; tests inject the fake:

```python
# Testable — clock is injectable
class TTLCache:
    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None: ...

# Hard to test — boundary buried in the implementation
class TTLCache:
    def _now(self) -> float:
        return time.monotonic()
```

**SDK-style interfaces over generic fetchers.** One function per external operation — each fake returns one specific shape, no conditional logic in test setup:

```python
# GOOD: each operation independently fakeable
class OrdersApi(Protocol):
    def get_user(self, user_id: str) -> User: ...
    def get_orders(self, user_id: str) -> list[Order]: ...

# BAD: faking requires conditionals on endpoint strings
class Api(Protocol):
    def request(self, endpoint: str, **kwargs: object) -> object: ...
```

## Fixture placement

Shared by 2+ test modules -> `conftest.py`. Single-use -> keep local to the test module (AGENTS.md rule — stops conftest becoming a dumping ground).
