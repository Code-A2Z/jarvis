import streamlit as st  # type: ignore
from src.helpers.structPages import structPages
from src.helpers.getFolders import getFolders


def application():
    pages = {
        "": [
            st.Page("src/apps/public/home.py",
                    title="Home", icon=":material/home:"),
            st.Page("src/apps/public/youtubePlaylist.py",
                    title="Jarvis Videos", icon=":material/ondemand_video:"),
        ],
        "Account": [
            st.Page("src/apps/auth/auth.py", title="Authentication",
                    icon=":material/lock_open:"),
        ],
    }

    # Check if st has the "user" attribute and if the user is logged in
    if hasattr(st, "user") and getattr(st.user, "is_logged_in", False):
        MAIN_DIR = "src/apps/pages"
        folders = getFolders(MAIN_DIR)
        if folders:
            for folder_name, folder_dir in folders.items():
                pages[folder_name.title()] = structPages(
                    f"{MAIN_DIR}/{folder_dir}")

    return st.navigation(pages)


application().run()
