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

# 📚 Data Collection Methodology

The dataset for Kotoba Signals was constructed using 50 question-and-answer pairs sourced from Yahoo! Chiebukuro (知恵袋). Each entry consists of a naturally occurring user question paired with a human-provided response from the platform.

To create a comparative baseline for analysis, each question was also independently answered using ChatGPT. This resulted in two parallel response sets for every prompt: one human-generated and one model-generated.

This structure enables direct comparison between human and AI responses across linguistic features, response strategies, and informational framing. The goal is to support downstream analysis of differences in tone, structure, and content generation between native human discourse and large language model outputs.


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
```text
kotoba-signals/
├── app/
│   └── kotoba_dash_app.py
│   ├── assets/
│       └── typography.css
├── data/
│   └── raw/
│       └── yahoo_questions.csv
├── notebooks/
│   └── kotoba_signals.ipynb
├── src/
│   ├── kotoba_preprocessing.py
│   ├── kotoba_features.py
└── README.md
```
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

For the "Test Your Own Japanese Text" box, the following sample text can be used. It is the openening paragraph to Natsumei Soseki's classic *Kokoro*, written in 1914.  
「私はその人を常に先生と呼んでいた。だからここでもただ先生と書くだけで本名は打ち明けない。これは世間を憚かる遠慮というよりも、その方が私にとって自然だからである。私はその人の記憶を呼び起こすごとに、すぐ『先生』といいたくなる。筆を執っても心持は同じ事である。よそよそしい頭文字などはとても使う気にならない。」

English Translation:  
"I always called him 'Sensei.' That is why, here too, I shall simply refer to him as Sensei and not reveal his real name. This is not out of any desire to avoid public scrutiny; rather, it is simply because that is the most natural way for me to address him. Whenever I recall memories of him, the word 'Sensei' springs immediately to mind, and the feeling is no different when I put pen to paper. I could not bring myself to use some impersonal initial."

---

# 📈 Intended Use

Educational and exploratory NLP tool for comparing human vs AI Japanese writing styles.
