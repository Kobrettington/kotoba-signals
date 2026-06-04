"""
kotoba_features.py

Feature engineering for:
- Connective density
- Sentence-ending diversity
- Pronoun density
- Kana/Kanji ratios
"""

import re
from collections import Counter

import numpy as np
import pandas as pd

from sudachipy import Dictionary

from src.kotoba_preprocessing import split_sentences


# Initialize tokenizer
tokenizer = Dictionary().create()


# ------------------------------------------------------------------
# Feature 2: Connective Density
# ------------------------------------------------------------------

CONNECTIVES = {
    "しかし",
    "ただし",
    "そのため",
    "したがって",
    "つまり",
    "一方で",
    "また",
    "さらに",
    "なお",
    "ゆえに",
    "なので",
}


def extract_connectives(text):

    if pd.isna(text):
        return []

    found = []

    for m in tokenizer.tokenize(text):

        surface = m.surface()
        base = m.dictionary_form()

        if surface in CONNECTIVES or base in CONNECTIVES:
            found.append(surface)

    return found


# ------------------------------------------------------------------
# Feature 3: Sentence Ending Diversity
# ------------------------------------------------------------------

def extract_sentence_endings(text):
    sentences = split_sentences(text)
    endings = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        endings.append(sentence[-10:])
    return endings


def normalize_ending(ending):

    return re.sub(
        r"[。！？\s]+",
        "",
        ending
    )


def ending_diversity(endings):
    if len(endings) == 0:
        return 0
    return len(set(endings)) / len(endings)


def ending_entropy(endings):
    if len(endings) == 0:
        return 0

    counts = Counter(endings)
    total = sum(counts.values())
    probabilities = [
        count / total
        for count in counts.values()
    ]

    return -sum(
        p * np.log2(p)
        for p in probabilities
    )


# ------------------------------------------------------------------
# Feature 4: Pronoun Density
# ------------------------------------------------------------------

PRONOUNS = {
    "私",
    "わたし",
    "僕",
    "ぼく",
    "俺",
    "おれ",
    "あなた",
    "君",
    "きみ",
    "お前",
    "人",
    "誰か",
    "自分",
}


def extract_pronouns(text):
    if pd.isna(text):
        return []
    found = []
    for m in tokenizer.tokenize(text):
        surface = m.surface()
        base = m.dictionary_form()
        if surface in PRONOUNS or base in PRONOUNS:
            found.append(surface)
    return found


# ------------------------------------------------------------------
# Feature 5: Kana/Kanji Ratios
# ------------------------------------------------------------------

def is_kanji(char):
    return "\u4e00" <= char <= "\u9fff"


def is_kana(char):
    return (
        "\u3040" <= char <= "\u309f"
        or
        "\u30a0" <= char <= "\u30ff"
    )


def kana_kanji_ratio(text):
    if pd.isna(text):
        return pd.Series(
            [0, 0, 0],
            index=[
                "kanji_ratio",
                "kana_ratio",
                "kanji_to_kana"
            ]
        )

    kanji = sum(
        is_kanji(c)
        for c in text
    )

    kana = sum(
        is_kana(c)
        for c in text
    )

    total = max(len(text), 1)

    return pd.Series(
        [
            kanji / total,
            kana / total,
            kanji / (kana + 1)
        ],
        index=[
            "kanji_ratio",
            "kana_ratio",
            "kanji_to_kana"
        ]
    )


# ------------------------------------------------------------------
# Master Feature Pipeline
# ------------------------------------------------------------------

def add_features(long_df):

    long_df = long_df.copy()

    # Connectives
    long_df["connectives"] = (
        long_df["text"]
        .apply(extract_connectives)
    )

    long_df["connective_count"] = (
        long_df["connectives"]
        .apply(len)
    )

    long_df["connective_density"] = (
        long_df["connective_count"]
        /
        long_df["token_count"].replace(0, 1)
    )

    # Sentence endings
    long_df["sentence_endings"] = (
        long_df["text"]
        .apply(extract_sentence_endings)
    )

    long_df["normalized_endings"] = (
        long_df["sentence_endings"]
        .apply(
            lambda endings: [
                normalize_ending(e)
                for e in endings
            ]
        )
    )

    long_df["ending_diversity"] = (
        long_df["normalized_endings"]
        .apply(ending_diversity)
    )

    long_df["ending_entropy"] = (
        long_df["normalized_endings"]
        .apply(ending_entropy)
    )

    # Pronouns
    long_df["pronouns"] = (
        long_df["text"]
        .apply(extract_pronouns)
    )

    long_df["pronoun_count"] = (
        long_df["pronouns"]
        .apply(len)
    )

    long_df["pronoun_density"] = (
        long_df["pronoun_count"]
        /
        long_df["token_count"].replace(0, 1)
    )

    # Kana/Kanji
    long_df[
        [
            "kanji_ratio",
            "kana_ratio",
            "kanji_to_kana"
        ]
    ] = (
        long_df["text"]
        .apply(kana_kanji_ratio)
    )

    return long_df
