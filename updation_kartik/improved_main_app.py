import streamlit as st
import logging
from typing import Dict, Any

from src.helpers.getFolders import getFolders
from src.helpers.structPages import structPages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_get_secret(key_path: str, default: Any = None) -> Any:
    """Safely retrieve secrets with proper error handling."""
    try:
        keys = key_path.split('.')
        value = st.secrets
        for key in keys:
            value = value[key]
        return value
    except (KeyError, AttributeError) as e:
        logger.warning(f"Secret key '{key_path}' not found: {e}")
        return default


def build_authenticated_pages() -> Dict[str, Any]:
    """Build pages for authenticated users with error handling."""
    pages = {}
    
    try:
        MAIN_DIR = "src/apps/pages"
        folders = getFolders(MAIN_DIR)
        
        if folders:
            for folder_name, folder_dir in folders.items():
                try:
                    pages[folder_name.title()] = structPages(f"{MAIN_DIR}/{folder_dir}")
                except Exception as e:
                    logger.error(f"Error loading pages for {folder_name}: {e}")
                    st.error(f"Failed to load {folder_name} section")
        
        # Add admin pages if user is admin
        admin_email = safe_get_secret("general.ADMIN_EMAIL")
        admin_name = safe_get_secret("general.ADMIN_NAME")
        
        if (admin_email and admin_name and 
            st.user.email == admin_email and 
            st.user.given_name == admin_name):
            pages["Admin"] = [
                st.Page("src/apps/auth/env.py", title="Environment Variables", icon=":material/security:")
            ]
            
    except Exception as e:
        logger.error(f"Error building authenticated pages: {e}")
        st.error("Failed to load some application sections")
    
    return pages


def application():
    """Main application with improved error handling."""
    try:
        pages = {
            "": [
                st.Page("src/apps/public/home.py", title="Home", icon=":material/home:"),
                st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:"),
            ],
            "Account": [
                st.Page("src/apps/auth/auth.py", title="Authentication", icon=":material/lock_open:"),
            ],
        }

        # Add authenticated user pages
        if st.user and st.user.is_logged_in:
            authenticated_pages = build_authenticated_pages()
            pages.update(authenticated_pages)

        return st.navigation(pages)
        
    except Exception as e:
        logger.error(f"Critical error in application setup: {e}")
        st.error("Application failed to initialize properly. Please refresh the page.")
        # Return minimal navigation as fallback
        return st.navigation({
            "": [st.Page("src/apps/public/home.py", title="Home", icon=":material/home:")]
        })


if __name__ == "__main__":
    try:
        app = application()
        if app:
            app.run()
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        st.error("Critical application error. Please contact support.")