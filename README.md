# 📊 Kotoba Signals

A linguistic analysis dashboard for exploring differences between human-written and AI-generated Japanese text.

This project combines natural language processing, feature engineering, and an interactive Dash web application to surface measurable stylistic differences in Japanese language production.

---

# 🧠 Project Overview

Kotoba Signals investigates whether AI-generated Japanese text can be distinguished from human-written text using structural and stylistic linguistic features.

The system analyzes text across multiple dimensions:

- syntactic structure
- lexical choice
- discourse markers
- orthographic composition
- sentence-level variation

The output is an interactive dashboard that allows users to explore how these signals differ across datasets.

---

# 📦 Key Features

## Text Processing Pipeline
- Japanese tokenization using SudachiPy
- Sentence segmentation using punctuation rules
- Structured transformation into analysis-ready datasets

## Linguistic Features
- Token count
- Connective density (logical flow markers like しかし, したがって)
- Pronoun density (self-reference patterns)
- Sentence ending diversity
- Sentence ending entropy
- Kana / Kanji ratios

---

# 📊 Interactive Dashboard

Built with Dash and Plotly:

### Core Controls
- Feature selection dropdown
- Label filter (Human / AI / All)
- Token-length filtering slider
- Free-text input for user analysis

### Visualizations
- Distribution comparison (box plots)
- Feature histograms
- 2D linguistic space scatter plot (entropy vs connective density)

---

# 🏗️ Project Structure

kotoba-signals/
├── app/
│   └── kotoba_dash_app.py
├── src/
│   ├── kotoba_preprocessing.py
│   ├── kotoba_features.py
├── data/
│   └── raw/
│       └── yahoo_questions.csv
├── notebooks/
│   └── kotoba_signals.ipynb
└── README.md

---

# 🚀 How to Run the App

## Install dependencies
pip install dash plotly pandas sudachipy sudachidict_core

## Run dashboard
python app/kotoba_dash_app.py

Open:
http://127.0.0.1:8050/

---

# 🧪 How It Works

1. Load dataset containing human and AI Japanese answers  
2. Tokenize and normalize text using SudachiPy  
3. Extract linguistic features  
4. Aggregate into structured dataframe  
5. Render interactive dashboard  

---

# 📈 Intended Use

Educational and exploratory NLP tool for comparing human vs AI Japanese writing styles.
