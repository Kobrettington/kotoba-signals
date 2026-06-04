📊 Kotoba Signals

A linguistic analysis dashboard for exploring differences between human-written and AI-generated Japanese text.

This project combines natural language processing, feature engineering, and an interactive Dash web application to surface measurable stylistic differences in Japanese language production.

🧠 Project Overview

Kotoba Signals investigates whether AI-generated Japanese text can be distinguished from human-written text using structural and stylistic linguistic features.

The system analyzes text across multiple dimensions:

syntactic structure
lexical choice
discourse markers
orthographic composition
sentence-level variation

The output is an interactive dashboard that allows users to explore how these signals differ across datasets.

📦 Key Features
🧾 Text Processing Pipeline
Japanese tokenization using SudachiPy
Sentence segmentation using punctuation rules
Structured transformation into analysis-ready datasets
🔬 Linguistic Features

The system extracts several interpretable features:

Token count
Connective density (logical flow markers like しかし, したがって)
Pronoun density (self-reference patterns)
Sentence ending diversity
Sentence ending entropy
Kana / Kanji ratios
📊 Interactive Dashboard

Built with Dash and Plotly, the application includes:

Core Controls
Feature selection dropdown
Label filter (Human / AI / All)
Token-length filtering slider
Free-text input for user analysis
Visualizations
Distribution comparison (box plots)
Feature histograms
2D linguistic space scatter plot (entropy vs connective density)
🏗️ Project Structure
kotoba-signals/
│
├── app/
│   └── kotoba_dash_app.py        # Dash web application
│
├── src/
│   ├── kotoba_preprocessing.py   # Tokenization + dataset prep
│   ├── kotoba_features.py        # Feature engineering
│
├── data/
│   └── raw/
│       └── yahoo_questions.csv   # Human + AI text dataset
│
├── notebooks/
│   └── analysis.ipynb            # Exploratory analysis
│
└── README.md
🚀 How to Run the App
1. Install dependencies
pip install dash plotly pandas sudachipy sudachidict_core
2. Run the dashboard

From the project root:

python app/kotoba_dash_app.py

Then open:

http://127.0.0.1:8050/
🧪 How It Works
Load dataset containing human and AI Japanese answers
Tokenize and normalize text using SudachiPy
Extract linguistic features at token, sentence, and character level
Aggregate features into structured dataframe
Render interactive visual analytics in Dash
📈 Intended Use

This project is designed for:

computational linguistics exploration
AI text detection research
feature engineering experimentation
educational visualization of Japanese NLP

It is not a production-grade classifier, but a feature-driven exploratory system.

⚠️ Notes
Performance depends on SudachiPy dictionary initialization
Dataset must contain human_answer and ai_answer columns
Designed for local execution and educational use
🧭 Future Extensions
Add supervised classification (human vs AI prediction model)
Expand feature set (dependency parsing, sentiment, style metrics)
Add real-time evaluation of user input text
Deploy as hosted web app



kotoba-signals/
│
├── data/
│   └── raw/
│       └── yahoo_questions.csv
│
├── notebooks/
│   └── 123.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── features.py
│   └── visualization.py
│
├── outputs/
│   ├── feature_table.csv
│   └── plots/
│
└── app/
    └── dash_app.py
