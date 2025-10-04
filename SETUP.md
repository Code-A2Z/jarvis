# How to run Jarvis locally

Welcome to the Jarvis Virtual Assistant! This guide will walk you through setting up the project on your local machine so you can explore features, understand the internal flow, and start contributing.

---

### 📋 Prerequisites

Ensure you have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/)
- [Git](https://git-scm.com/downloads)
- [Streamlit](https://docs.streamlit.io/)

**Optional but recommended:**
- A virtual environment tool like `venv` or `virtualenv`

---

### 📦 Clone the Repository

```bash
git clone https://github.com/Code-A2Z/jarvis.git
cd jarvis
```

---

### 🧰 Install uv

#### ▶️ Windows

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 🐧 macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### 🧪 Install Dependencies

```bash
uv sync
```

---

### 🔐 Configure `.streamlit/secrets.toml`

If the `.streamlit` folder doesn't exist, create it:

```bash
mkdir .streamlit
```

Then create a file named `secrets.toml` inside `.streamlit` and **add the following fields only** (as per maintainer's request):

```toml
[general]
ADMIN_EMAIL = ""
ADMIN_NAME = ""

[auth]
redirect_uri = ""
cookie_secret = ""

[auth.google]
client_id = ""
client_secret = ""
server_metadata_url = ""
```

> 🔒 Keep this file private. Never commit secrets to the repository.

---

### 🧪 Mock Authentication (Optional)

To test features without logging in via Google, you can mock a user manually.

In `home.py`, add:

```python
st.session_state.user = {
    "name": "Test User",
    "email": "test@example.com"
}
```

This will let you access all core features locally during development.

---

### 🚀 Run Jarvis

Launch the application:

```bash
uv run streamlit run src/apps/public/home.py
```

It should open in your browser at `http://localhost:8501`.

---

### 🛠️ Common Errors & Fixes

- `ModuleNotFoundError`: Make sure the virtual environment is activated and dependencies installed.
- `secrets.toml not found`: Ensure `.streamlit/secrets.toml` exists and is correctly formatted.
- `Google login not working`: Re-check your `client_id`, `client_secret`, and `redirect_uri`.

---

### 🤝 Want to Contribute?

- Review the [Contribution Guidelines](CONTRIBUTING.md)
- Join our [Discord Community](https://discord.gg/tSqtvHUJzE)
- Raise an issue or PR with a clear description
- Follow the project’s [Code of Conduct](CODE_OF_CONDUCT.md)

---

Happy coding! 💻✨ Let Jarvis assist you.
