import contextlib
import io
import os
import sys
from pathlib import Path

from instagrapi import Client

USERNAME = os.getenv("INSTAGRAM_USERNAME", "").strip()
PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
CHALLENGE_CODE = os.getenv("INSTAGRAM_CHALLENGE_CODE", "").strip()
SESSION_FILE = Path(os.getenv("INSTAGRAM_SESSION_FILE", "session.json"))


def main() -> int:
    if not USERNAME or not PASSWORD:
        print(
            "Missing GitHub Actions secrets: add INSTAGRAM_USERNAME and "
            "INSTAGRAM_PASSWORD under Settings > Secrets and variables > Actions.",
            file=sys.stderr,
        )
        return 2

    if CHALLENGE_CODE and (
        len(CHALLENGE_CODE) != 6 or not CHALLENGE_CODE.isdigit()
    ):
        print(
            "INSTAGRAM_CHALLENGE_CODE must be exactly 6 digits.",
            file=sys.stderr,
        )
        return 2

    client = Client()

    def challenge_code_handler(username, choice):
        if not CHALLENGE_CODE:
            raise RuntimeError(
                "Instagram requested a verification code. Add the latest "
                "6-digit email code as the INSTAGRAM_CHALLENGE_CODE GitHub "
                "secret, then run this workflow again."
            )
        return CHALLENGE_CODE

    client.challenge_code_handler = challenge_code_handler

    try:
        if SESSION_FILE.is_file():
            client.load_settings(str(SESSION_FILE))
            print("Found an existing session; validating it...")

        # Suppress library output because some versions print the verification code.
        with contextlib.redirect_stdout(io.StringIO()):
            client.login(USERNAME, PASSWORD)

        client.dump_settings(str(SESSION_FILE))

        try:
            SESSION_FILE.chmod(0o600)
        except OSError:
            pass

        print(f"Login successful. Session saved to: {SESSION_FILE}")
        print(f"Instagram User ID: {client.user_id}")
        return 0

    except Exception as exc:
        # Never print credentials, verification codes, request headers, or session data.
        print(
            f"Instagram login/session creation failed: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
