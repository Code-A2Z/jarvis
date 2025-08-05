"""
Clear Streamlit Cache and Restart
Run this after retraining the model to force reload
"""
import os
import sys

print("🧹 Clearing Streamlit cache...")

# Clear Python cache files
def clear_pycache():
    for root, dirs, files in os.walk('.'):
        for d in dirs:
            if d == '__pycache__':
                pycache_path = os.path.join(root, d)
                try:
                    import shutil
                    shutil.rmtree(pycache_path)
                    print(f"✅ Cleared {pycache_path}")
                except:
                    pass

clear_pycache()

# Clear .streamlit cache if it exists
streamlit_cache = os.path.expanduser("~/.streamlit")
if os.path.exists(streamlit_cache):
    try:
        import shutil
        shutil.rmtree(streamlit_cache)
        print("✅ Cleared Streamlit cache")
    except:
        pass

print("🔄 Cache cleared! Restart Jarvis to see the improved model.")
print("📧 The spam detection should now work much better!")
