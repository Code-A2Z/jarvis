# House Price Prediction (Jarvis)

This is a small, self-contained house price prediction example (Level 2). It includes:
- A reproducible training & evaluation script (`housePricePrediction.py`).
- Optional Streamlit demo (`housePricePrediction_streamlit.py`).
- A tiny example dataset in `examples/` for quick smoke tests.

**Dataset:** Use the included sample for quick tests. For full training, the maintainer should download the full **Ames Housing dataset** (link provided below).

## How to run (quick)
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run training + evaluation:
   ```bash
   python housePricePrediction.py
   ```
4. Optional streamlit demo:
   ```bash
   streamlit run housePricePrediction_streamlit.py
   ```
## Dataset links
- Ames Housing dataset on Kaggle (recommended): https://www.kaggle.com/c/house-prices-advanced-regression-techniques
*(NOTE: Do not commit large model files (like `house_price_model_joblib.pkl`) or the full dataset.)*
