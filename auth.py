"""Login handling for TaskFlow, including lockout after repeated failures."""
from werkzeug.security import check_password_hash, generate_password_hash

from utils import attempt_tracker

MAX_ATTEMPTS = 3
LOCKOUT_SECONDS = 5 * 60

# Toy user directory. A real app would back this with a database.
USERS = {
    "admin": generate_password_hash("admin"),
    "alice": generate_password_hash("wonderland"),
    "bob": generate_password_hash("builder123"),
}

# Tracks failed login attempts per username. Passed into attempt_tracker,
# which is generic enough to reuse for e.g. password-reset attempts too.
_login_attempts = {}


def authenticate(username, password):
    """Validate credentials, enforcing lockout after MAX_ATTEMPTS failures.

    Returns a (success, error_message) tuple. error_message is None on
    success.
    """
    if attempt_tracker(_login_attempts, username, "check", MAX_ATTEMPTS, LOCKOUT_SECONDS):
        return False, "Account locked due to too many failed attempts. Try again later."

    password_hash = USERS.get(username)
    if password_hash and check_password_hash(password_hash, password):
        attempt_tracker(_login_attempts, username, "success")
        return True, None

    locked_now = attempt_tracker(_login_attempts, username, "failure", MAX_ATTEMPTS, LOCKOUT_SECONDS)
    if locked_now:
        return False, "Account locked due to too many failed attempts. Try again later."
    return False, "Invalid username or password."
