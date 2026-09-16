"""
GenerateArtifacts.py

Generate artifacts from the TSA Scrum dataset

Artifacts:
    1. Feature correlation heatmap
    2. TSA distribution by performance
    3. Sentiment by performance
    4. Turn-taking by performance
    5. Random Forest feature importance
    6. Confusion matrix
    7. Model performance comparison
    8. TSA progression by sprint

Author: Benjamin Davis
"""

from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------


DATA_FILE = "clean_data_scrum.pickle"
PREDICTION_FILE = "prediction_w_sentiment_df.pickle"
OUTPUT_DIR = Path("diagrams/generated")

DPI = 300
RANDOM_STATE = 42

PERFORMANCE_LABELS = {
    1: "Low",
    2: "Medium",
    3: "High"
}

TSA_LABELS = {
    3: "Perception",
    4: "Comprehension",
    5: "Projection",
    6: "Action"
}

# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------

def setup():
    """Configure plotting and create the output directory."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")

    plt.rcParams.update({
        "figure.dpi": 100,
        "savefig.dpi": DPI,
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "figure.titlesize": 16
    })

def load_pickle(filename):
# Load a pickle file.

    with open(filename, "rb") as handle:
        return pickle.load(handle)


def save_figure(filename):
# Save the current matplotlib figure.

    output_path = OUTPUT_DIR / filename

    plt.tight_layout()
    plt.savefig(
        output_path,
        dpi=DPI,
        bbox_inches="tight"
    )

    print(f"Saved: {output_path}")

# ---------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------

def add_aggregate_features(df):

# Create aggregate features that are easier to interpret
# than individual-player features.


    df = df.copy()

    tsa_average_columns = [
        col for col in df.columns
        if "SA Average" in col
    ]

    if tsa_average_columns:
        df["Mean TSA"] = df[tsa_average_columns].mean(axis=1)

    tsa_turn_columns = [
        "SA 3 Turn Taking",
        "SA 4 Turn Taking",
        "SA 5 Turn Taking",
        "SA 6 Turn Taking"
    ]

    existing_columns = [
        col for col in tsa_turn_columns
        if col in df.columns
    ]

    if existing_columns:

        total_tsa = df[existing_columns].sum(axis=1)

        # Avoid divide-by-zero errors
        total_tsa = total_tsa.replace(0, np.nan)

        for tsa in range(3, 7):

            column = f"SA {tsa} Turn Taking"

            if column in df.columns:
                df[f"TSA {tsa} %"] = (
                    df[column] / total_tsa
                ) * 100

    return df


# ---------------------------------------------------------
# Artifact 1:
# Correlation Heatmap
# ---------------------------------------------------------

def generate_correlation_heatmap(df):

    desired_features = [
        "Number of Turns",
        "Average Turn Taking",
        "Mean TSA",
        "TSA 3 %",
        "TSA 4 %",
        "TSA 5 %",
        "TSA 6 %",
        "Mean Sentiment",
        "Delta Sentiment",
        "Performance Rank"
    ]

    features = [
        col for col in desired_features
        if col in df.columns
    ]

    correlation = df[features].corr()

    plt.figure(figsize=(11, 9))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5
    )

    plt.title(
        "Correlation Between Scrum Communication Features"
    )

    save_figure("01_feature_correlation_heatmap.png")

    plt.close()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("\nGenerating thesis artifacts...\n")

    setup()

    prediction_df = load_pickle(
        PREDICTION_FILE
    )

    raw_data = load_pickle(
        DATA_FILE
    )

    prediction_df = add_aggregate_features(
        prediction_df
    )

    # Descriptive artifacts
    generate_correlation_heatmap(
        prediction_df
    )

    # generate_tsa_distribution(
    #     prediction_df
    # )

    # generate_sentiment_plot(
    #     prediction_df
    # )

    # generate_turn_taking_plot(
    #     prediction_df
    # )

    # # Machine-learning artifacts
    # X_train, X_test, y_train, y_test = (
    #     prepare_ml_data(prediction_df)
    # )

    # random_forest = generate_feature_importance(
    #     X_train,
    #     X_test,
    #     y_train,
    #     y_test
    # )

    # generate_confusion_matrix(
    #     random_forest,
    #     X_test,
    #     y_test
    # )

    # generate_model_comparison(
    #     X_train,
    #     X_test,
    #     y_train,
    #     y_test
    # )

    # # Temporal artifact
    # generate_sprint_progression(
    #     raw_data,
    #     prediction_df
    # )

    print(
        f"\nFinished. Artifacts saved to: "
        f"{OUTPUT_DIR.resolve()}"
    )


if __name__ == "__main__":
    main()