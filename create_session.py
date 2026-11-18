import json
import os
import sys
from pathlib import Path

from instagrapi import Client

SESSION_JSON = os.getenv("INSTAGRAM_SESSION_JSON", "")
SESSION_FILE = Path(os.getenv("INSTAGRAM_SESSION_FILE", "session.json"))


def main() -> int:
    if not SESSION_JSON.strip():
        print(
            "Missing INSTAGRAM_SESSION_JSON. Export the working Instagram "
            "session from your trusted computer, then save the complete "
            "session.json contents as a GitHub Actions repository secret "
            "named INSTAGRAM_SESSION_JSON.",
            file=sys.stderr,
        )
        return 2

    try:
        # Parse and validate the secret without printing its contents.
        settings = json.loads(SESSION_JSON)
        if not isinstance(settings, dict) or not settings:
            raise ValueError("The session JSON must be a non-empty object.")

        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        SESSION_FILE.write_text(
            json.dumps(settings, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        try:
            SESSION_FILE.chmod(0o600)
        except OSError:
            pass

        client = Client()
        client.load_settings(str(SESSION_FILE))

        print("Session settings imported successfully.")
        print(f"Session file created: {SESSION_FILE}")
        print("No Instagram password login or verification challenge was attempted.")
        return 0

    except Exception as exc:
        print(
            f"Session import failed: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
