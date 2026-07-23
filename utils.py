"""Shared helper functions used across TaskFlow."""
import time
from functools import wraps

from flask import redirect, session, url_for


def login_required(view_func):
    """Redirect to the login page unless a user is logged in."""

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped


def attempt_tracker(store, key, action, max_attempts=3, lockout_seconds=300):
    """Generic failed-attempt / lockout tracker.

    `store` is a dict owned by the caller (e.g. failed login attempts or
    password reset attempts), keyed by whatever identifies the actor
    (username, email, IP, ...). `action` is one of "check", "success", or
    "failure". Returns True if `key` is currently locked out after the
    action is applied.
    """
    now = time.time()
    entry = store.get(key)
    if entry and entry.get("locked_until") and now >= entry["locked_until"]:
        entry = None
    if entry is None:
        entry = {"failures": 0, "locked_until": None}

    if action == "success":
        store.pop(key, None)
        return False

    if action == "failure":
        entry["failures"] += 1
        if entry["failures"] >= max_attempts:
            entry["locked_until"] = now + lockout_seconds
        store[key] = entry
        return bool(entry["locked_until"] and now < entry["locked_until"])

    # action == "check": look without recording anything
    store[key] = entry
    return bool(entry["locked_until"] and now < entry["locked_until"])


def cached_lookup(cache, key, loader, ttl_seconds=5):
    """Simple TTL cache: returns `loader()`, caching the result under `key`
    for `ttl_seconds`. `cache` is a dict owned by the caller, so this can be
    reused for other read-heavy lookups beyond just tasks.
    """
    now = time.time()
    entry = cache.get(key)
    if entry and now - entry["cached_at"] < ttl_seconds:
        return entry["value"]

    value = loader()
    cache[key] = {"value": value, "cached_at": now}
    return value


def invalidate_cache(cache, key):
    """Drop a cached entry so the next `cached_lookup` call re-fetches it."""
    cache.pop(key, None)
