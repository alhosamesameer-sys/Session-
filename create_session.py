import os
import sys
from pathlib import Path

from instagrapi import Client

USERNAME = os.getenv("INSTAGRAM_USERNAME", "").strip()
PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
SESSION_FILE = Path(os.getenv("INSTAGRAM_SESSION_FILE", "session.json"))


def main() -> int:
    if not USERNAME or not PASSWORD:
        print(
            "Missing GitHub Actions secrets: add INSTAGRAM_USERNAME and "
            "INSTAGRAM_PASSWORD under Settings > Secrets and variables > Actions.",
            file=sys.stderr,
        )
        return 2

    client = Client()

    try:
        if SESSION_FILE.is_file():
            client.load_settings(str(SESSION_FILE))
            print("Found an existing session; validating it...")

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
        # Do not print credentials, request headers, or session data.
        print(f"Instagram login/session creation failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
