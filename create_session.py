import os
from pathlib import Path

from instagrapi import Client

USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
SESSION_FILE = Path(os.getenv("INSTAGRAM_SESSION_FILE", "session.json"))


def main():
    if not USERNAME or not PASSWORD:
        raise SystemExit(
            "يرجى ضبط INSTAGRAM_USERNAME و INSTAGRAM_PASSWORD كمتغيرات بيئة أولاً."
        )

    cl = Client()

    try:
        if SESSION_FILE.is_file():
            cl.load_settings(str(SESSION_FILE))
            print("تم العثور على جلسة محفوظة؛ جارٍ التحقق منها...")

        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(str(SESSION_FILE))

        try:
            SESSION_FILE.chmod(0o600)
        except OSError:
            pass

        print(f"تم تسجيل الدخول وحفظ/تحديث الجلسة: {SESSION_FILE}")
        print(f"Instagram User ID: {cl.user_id}")

    except Exception as exc:
        print(f"تعذّر تسجيل الدخول أو حفظ الجلسة: {type(exc).__name__}: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
