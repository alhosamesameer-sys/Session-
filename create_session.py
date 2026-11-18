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
            "Missing INSTAGRAM_USERNAME or INSTAGRAM_PASSWORD. "
            "Add both as GitHub Actions repository secrets.",
            file=sys.stderr,
        )
        return 2

    try:
        client = Client()
        client.login(USERNAME, PASSWORD)

        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        client.dump_settings(str(SESSION_FILE))
        try:
            SESSION_FILE.chmod(0o600)
        except OSError:
            pass

        print("Instagram login succeeded and a new session was saved.")
        print(f"Session file created: {SESSION_FILE}")
        return 0

    except Exception as exc:
        print(
            f"Instagram session creation failed: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
