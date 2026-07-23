"""Tests for auth.py: login success, login failure, and lockout behavior."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import auth


@pytest.fixture(autouse=True)
def reset_login_attempts():
    auth._login_attempts.clear()
    yield
    auth._login_attempts.clear()


def test_login_success():
    success, error = auth.authenticate("alice", "wonderland")
    assert success is True
    assert error is None


def test_login_failure_wrong_password():
    success, error = auth.authenticate("alice", "wrong-password")
    assert success is False
    assert error == "Invalid username or password."


def test_login_failure_unknown_user():
    success, error = auth.authenticate("nobody", "whatever")
    assert success is False
    assert error == "Invalid username or password."


def test_account_locks_after_max_attempts():
    for _ in range(auth.MAX_ATTEMPTS - 1):
        success, error = auth.authenticate("bob", "wrong")
        assert success is False
        assert error == "Invalid username or password."

    # This failure hits the limit and triggers the lockout.
    success, error = auth.authenticate("bob", "wrong")
    assert success is False
    assert "locked" in error.lower()

    # Even the correct password is rejected while locked out.
    success, error = auth.authenticate("bob", "builder123")
    assert success is False
    assert "locked" in error.lower()


def test_successful_login_resets_attempt_count():
    auth.authenticate("alice", "wrong")
    auth.authenticate("alice", "wrong")
    success, error = auth.authenticate("alice", "wonderland")
    assert success is True

    # Attempt count should have reset by the success above, so this single
    # fresh failure shouldn't trigger a lockout (limit is 3).
    success, error = auth.authenticate("alice", "wrong")
    assert success is False
    assert error == "Invalid username or password."
