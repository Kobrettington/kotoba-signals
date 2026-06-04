import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ----------------------------
# Path setup
# ----------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.kotoba_preprocessing import preprocess_dataset
from src.kotoba_features import add_features

# ----------------------------
# Load + preprocess data
# ----------------------------

file_path = PROJECT_ROOT / "data" / "raw" / "yahoo_questions.csv"

long_df, token_df = preprocess_dataset(file_path)
long_df = add_features(long_df)

# ----------------------------
# Dash app
# ----------------------------

app = Dash(__name__)

# ----------------------------
# App layout (NARRATIVE INCLUDED)
# ----------------------------

app.layout = html.Div([
    
    html.H1("Kotoba Signal Explorer"),
    
    html.P("""
        This dashboard explores linguistic differences between human-written
        and AI-generated Japanese text using structural and stylistic signals.
        """),

    html.Hr(),

    # ------------------------
    # COMPONENT 1: Dropdown
    # ------------------------
    html.Label("Select Feature"),
    dcc.Dropdown(
        id="feature-dropdown",
        options=[
            {"label": "Token Count", "value": "token_count"},
            {"label": "Connective Density", "value": "connective_density"},
            {"label": "Ending Entropy", "value": "ending_entropy"},
            {"label": "Pronoun Density", "value": "pronoun_density"},
            {"label": "Kana Ratio", "value": "kana_ratio"},
            {"label": "Kanji Ratio", "value": "kanji_ratio"},
        ],
        value="token_count"
    ),

    html.Br(),

    # ------------------------
    # COMPONENT 2: Radio buttons
    # ------------------------
    html.Label("Filter by Label"),
    dcc.RadioItems(
        id="label-filter",
        options=[
            {"label": "All", "value": "all"},
            {"label": "Human", "value": "human"},
            {"label": "AI", "value": "ai"},
        ],
        value="all"
    ),

    html.Br(),

    # ------------------------
    # COMPONENT 3: Slider
    # ------------------------
    html.Label("Minimum Token Count"),
    dcc.Slider(
        id="token-slider",
        min=0,
        max=int(long_df["token_count"].max()),
        step=5,
        value=0
    ),

    html.Br(),

    # ------------------------
    # COMPONENT 4: Text input
    # ------------------------
    html.Label("Test Your Own Japanese Text"),

        dcc.Textarea(
            id="user-text",
            placeholder="Enter Japanese text here...",
            style={"width": "100%", "height": 100}
        ),

        html.Div(
            id="user-analysis-output",
            style={
                "marginTop": "15px",
                "padding": "15px",
                "backgroundColor": "#f8f9fa",
                "border": "1px solid #ddd",
                "borderRadius": "8px"
            }
        ),

        html.Hr(),

    # ------------------------
    # Graphs
    # ------------------------

    html.H3("Feature Comparison"),

    html.P(
        "Compares the selected linguistic feature between human-written and "
        "AI-generated texts. The box plot highlights differences in typical "
        "values, variability, and outliers for each group."
    ),

    dcc.Graph(id="distribution-plot"),

    html.H3("Linguistic Space"),

    html.P(
        "Plots each text according to its sentence-ending entropy and "
        "connective density. Clusters or separation between human and AI "
        "texts may reveal distinct stylistic patterns and writing behaviors."
    ),

    dcc.Graph(id="pca-plot"),

    html.H3("Feature Distribution"),

    html.P(
        "Displays how frequently different values of the selected feature "
        "occur across the dataset. Comparing the human and AI distributions "
        "helps identify whether one group tends to use the feature more often "
        "or more consistently."
    ),

dcc.Graph(id="histogram-plot"),

    html.Hr(),

])

# ----------------------------
# CALLBACK 1: Main plots
# ----------------------------

@app.callback(
    Output("distribution-plot", "figure"),
    Output("pca-plot", "figure"),
    Output("histogram-plot", "figure"),
    Input("feature-dropdown", "value"),
    Input("label-filter", "value"),
    Input("token-slider", "value")
)
def update_graphs(feature, label, min_tokens):

    df = long_df.copy()
    df = df[df["token_count"] >= min_tokens]

    if label != "all":
        df = df[df["label"] == label]

    # ------------------------
    # Plot 1: distribution by label
    # ------------------------
    fig1 = px.box(
        df,
        x="label",
        y=feature,
        color="label",
        title=f"{feature} by Label"
    )

    # ------------------------
    # Plot 2: PCA scatter (simple version)
    # ------------------------
    fig2 = px.scatter(
        df,
        x="ending_entropy",
        y="connective_density",
        color="label",
        title="Linguistic Space (Entropy vs Connectives)"
    )

    # ------------------------
    # Plot 3: histogram
    # ------------------------
    fig3 = px.histogram(
        df,
        x=feature,
        color="label",
        barmode="overlay",
        opacity=0.6,
        title=f"Distribution of {feature}"
    )

    return fig1, fig2, fig3


# ----------------------------
# CALLBACK 2: user text analysis
# ----------------------------

@app.callback(
    Output("user-analysis-output", "children"),
    Input("user-text", "value")
)
def analyze_user_text(text):

    if not text:
        return "Enter text above to analyze."

    from src.kotoba_features import (
        extract_connectives,
        extract_pronouns
    )

    connectives = extract_connectives(text)
    pronouns = extract_pronouns(text)

    return html.Div([
        html.H4("Your Text Analysis"),
        html.P(f"Connectives found: {connectives}"),
        html.P(f"Pronouns found: {pronouns}")
    ])


# ----------------------------
# RUN APP
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)
