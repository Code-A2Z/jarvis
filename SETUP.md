# 🛠️ SETUP.md – How to Set Up Jarvis Locally

Welcome to the Jarvis Virtual Assistant! This guide will walk you through setting up the project on your local machine so you can explore features, understand the internal flow, and start contributing.

---

## 📋 Prerequisites

Ensure you have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/downloads)
- [Streamlit](https://docs.streamlit.io/)

**Optional but recommended:**
- A virtual environment tool like `venv` or `virtualenv`

---

## 🔻 Clone the Repository

```bash
git clone https://github.com/Code-A2Z/jarvis.git
cd jarvis
```

---

## 🧪 Set Up a Virtual Environment (Optional but Recommended)

### ▶️ Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 🐧 macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Install Dependencies

Install all required Python packages using:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configure `.streamlit/secrets.toml`

Create a `.streamlit` folder in the root if it doesn’t exist:

```bash
mkdir .streamlit
```

Then create a file named `secrets.toml` inside `.streamlit`:

```toml
[general]
ADMIN_EMAIL = "youremail@example.com"
ADMIN_NAME = "Your Name"

[auth]
GOOGLE_CLIENT_ID = "your-google-client-id"
GOOGLE_CLIENT_SECRET = "your-google-client-secret"
```

> You can find your client ID and secret by creating OAuth credentials in your Google Developer Console.

---

## 🧪 Running in Mock Mode (Optional)

To test features without login, Jarvis supports a mock mode. This allows you to bypass Google Auth while developing.

```bash
streamlit run jarvis.py --mock
```

This uses a file named `mock_user.py` to simulate a logged-in user.

---

## 🚀 Run Jarvis

Once setup is done, run the project:

```bash
streamlit run jarvis.py
```

Or to test without authentication:

```bash
streamlit run jarvis.py --mock
```

This should open the app in your browser at `http://localhost:8501`.

---

## 🐞 Troubleshooting

- `ModuleNotFoundError`: Make sure the virtual environment is activated and you're inside the cloned `jarvis` directory.
- `secrets.toml not found`: Ensure `.streamlit/secrets.toml` exists with correct credentials.
- `Google Auth Not Working`: Try using `--mock` flag or check your client credentials.

---

## 🤝 Want to Contribute?

- Make sure you've read the [Contribution Guidelines](CONTRIBUTING.md)
- Choose an issue from [GitHub Issues](https://github.com/Code-A2Z/jarvis/issues)
- Join our community on [Discord](https://discord.gg/tSqtvHUJzE)
- Raise a PR and tag the maintainers when ready!

---

Happy contributing! 💻✨