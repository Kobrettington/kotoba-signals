# 1. Feature table builder
def build_feature_table(long_df):
    return long_df[[
        "id",
        "label",
        "token_count",
        "connective_density",
        "ending_entropy",
        "pronoun_density",
        "sent_len_mean",
        "sent_len_std",
        "kanji_ratio",
        "kana_ratio"
    ]].copy()

# 2. Normalization
from sklearn.preprocessing import StandardScaler

def normalize_features(df, features):
    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])
    return df, scaler

# 3. PCA projection
from sklearn.decomposition import PCA

def compute_pca(df, features):
    pca = PCA(n_components=2)
    proj = pca.fit_transform(df[features])
    
    df["pca1"] = proj[:, 0]
    df["pca2"] = proj[:, 1]
    
    return df, pca

# 4. Plot helper
import matplotlib.pyplot as plt

def plot_pca(df):
    plt.figure()
    
    for label in df["label"].unique():
        subset = df[df["label"] == label]
        plt.scatter(subset["pca1"], subset["pca2"], label=label)
    
    plt.legend()
    plt.title("Human vs AI (PCA Projection)")
    plt.show()
