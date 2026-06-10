import pytest

from ttlcache.cache import TTLCache


class FakeClock:
    """Hand-written fake for the time boundary."""

    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def cache(clock: FakeClock) -> TTLCache[str, int]:
    return TTLCache(clock=clock)


def test_get_before_expiry(cache: TTLCache[str, int], clock: FakeClock) -> None:
    cache.set("a", 1, ttl=10)
    clock.advance(9.9)
    assert cache.get("a") == 1


def test_get_after_expiry_returns_default(cache: TTLCache[str, int], clock: FakeClock) -> None:
    cache.set("a", 1, ttl=10)
    clock.advance(10.1)
    assert cache.get("a") is None


def test_missing_key_returns_default(cache: TTLCache[str, int]) -> None:
    assert cache.get("missing", default=-1) == -1


def test_overwrite_resets_ttl(cache: TTLCache[str, int], clock: FakeClock) -> None:
    cache.set("a", 1, ttl=10)
    clock.advance(8)
    cache.set("a", 2, ttl=10)
    clock.advance(8)
    assert cache.get("a") == 2


def test_len_counts_only_live_entries(cache: TTLCache[str, int], clock: FakeClock) -> None:
    cache.set("a", 1, ttl=5)
    cache.set("b", 2, ttl=50)
    clock.advance(20)
    assert len(cache) == 1


def test_nonpositive_ttl_raises(cache: TTLCache[str, int]) -> None:
    with pytest.raises(ValueError, match="ttl must be positive"):
        cache.set("a", 1, ttl=0)
