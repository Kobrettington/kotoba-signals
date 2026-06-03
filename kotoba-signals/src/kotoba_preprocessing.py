# -------
# 1. Imports
from pathlib import Path
import re
import pandas as pd
from sudachipy import Dictionary


# 2. Initialize tokenizer
tokenizer = Dictionary().create()


# 3. Core text functions
# 3.1 Sentence splitter
def split_sentences(text):
    if pd.isna(text):
        return []

    sentences = re.split(r"[。！？]+", text)
    return [s.strip() for s in sentences if s.strip()]

# 3.2 Tokenizer
def tokenize(text):
    if pd.isna(text):
        return []

    return [m.surface() for m in tokenizer.tokenize(text)]

# 3.3 POS inspection helper
def inspect_tokens(text):
    tokens = tokenizer.tokenize(text)

    for m in tokens:
        print(
            "SURFACE:", m.surface(),
            "| BASE:", m.dictionary_form(),
            "| POS:", m.part_of_speech()
        )

# 3.4 Sentence token lengths
def sentence_token_lengths(text):
    sentences = split_sentences(text)

    lengths = []

    for sent in sentences:
        tokens = tokenize(sent)
        lengths.append(len(tokens))

    return lengths


# 4. Dataset loading
def load_dataset(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return pd.read_csv(file_path)


# 5. Build long format dataset
def create_long_dataframe(df):
    
    df["human_tokens"] = df["human_answer"].apply(tokenize)
    df["ai_tokens"] = df["ai_answer"].apply(tokenize)

    df["human_token_count"] = df["human_tokens"].apply(len)
    df["ai_token_count"] = df["ai_tokens"].apply(len)

    human_df = df[
        ["id", "human_answer", "human_tokens", "human_token_count"]
    ].copy()

    human_df["label"] = "human"

    human_df = human_df.rename(columns={
        "human_answer": "text",
        "human_tokens": "tokens",
        "human_token_count": "token_count"
    })

    ai_df = df[
        ["id", "ai_answer", "ai_tokens", "ai_token_count"]
    ].copy()

    ai_df["label"] = "ai"

    ai_df = ai_df.rename(columns={
        "ai_answer": "text",
        "ai_tokens": "tokens",
        "ai_token_count": "token_count"
    })

    long_df = pd.concat(
        [human_df, ai_df],
        ignore_index=True
    )

    return long_df


# 6. Add sentence information
def add_sentence_features(long_df):

    long_df = long_df.copy()

    long_df["sentences"] = (
        long_df["text"]
        .apply(split_sentences)
    )

    long_df["sentence_token_lengths"] = (
        long_df["text"]
        .apply(sentence_token_lengths)
    )

    return long_df


# 7. Token dataframe
def create_token_dataframe(long_df):

    token_rows = []

    for _, row in long_df.iterrows():

        for tok in row["tokens"]:

            token_rows.append({
                "id": row["id"],
                "label": row["label"],
                "token": tok
            })

    return pd.DataFrame(token_rows)

# 8. Master preprocessing pipeline
def preprocess_dataset(file_path):

    df = load_dataset(file_path)

    long_df = create_long_dataframe(df)

    long_df = add_sentence_features(long_df)

    token_df = create_token_dataframe(long_df)

    return long_df, token_df
