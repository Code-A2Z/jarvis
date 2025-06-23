from datetime import datetime
import streamlit as st  # type: ignore
from time import sleep
import pytz
import toml  # type: ignore
import types
from src.utils.greeting import GreetUser

# ────────────────────────────────────────────────────────────
# 1) Local‐dev stubs for st.user / st.login / st.logout
#    so you never hit StreamlitAuthError when you run this app locally.
if not hasattr(st, "user"):
    st.user = types.SimpleNamespace(
        is_logged_in=False,
        given_name="Developer",
        name="Local Dev",
        email="dev@example.com",
        picture="https://via.placeholder.com/150",
    )

try:
    with open("secrets.example.toml", "r") as f:
        secrets = toml.load(f)
except FileNotFoundError:
    secrets = {}

# Check if real Google creds are configured in secrets.toml
google_cfg = secrets.get("google", {})
if not google_cfg.get("clientId") or not google_cfg.get("clientSecret"):
    # No OAuth creds → stub out login/logout
    def _dummy_login(provider: str):
        st.user.is_logged_in = True

    def _dummy_logout():
        st.user.is_logged_in = False

    st.login = _dummy_login
    st.logout = _dummy_logout
# ────────────────────────────────────────────────────────────


def unix_to_ist(timestamp: float) -> str:
    india_tz = pytz.timezone("Asia/Kolkata")
    fmt = '%I:%M:%S %p IST'
    return (
        datetime.fromtimestamp(timestamp, pytz.utc)
        .astimezone(india_tz)
        .strftime(fmt)
    )


def auth():
    user = st.user

    if not user.is_logged_in:
        st.title("🔐 Login Required")
        st.write(
            "Please authenticate using your Google account to access your profile.")
        if st.button("🔓 Authenticate with Google"):
            st.login("google")

    else:
        st.title(f"🙏 {GreetUser(user.given_name)}")
        st.success("Welcome to Jarvis AI Assistant!", icon="🤝")
        st.image(user.picture, caption=user.name)
        st.write("Email:", user.email)

        if st.button("Log out"):
            st.toast(f"Goodbye, {user.name}! See you soon!", icon="🚪")
            sleep(2)
            st.logout()


auth()
