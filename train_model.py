"""
Train ML model for Reel vs Non-Reel traffic classification
-----------------------------------------------------------
Usage:
    python train_model.py --data datasets/traffic_dataset.csv
"""

import argparse
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

from src.reel_traffic_detection.data.preprocess import Preprocessor


def main(args):
    # Load dataset
    df = pd.read_csv(args.data)
    print(f"✅ Loaded dataset with {df.shape[0]} rows and {df.shape[1]} cols")

    # Train/test split
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["label"]
    )

    # Preprocessor
    pre = Preprocessor()
    pre.fit(train_df, label_column="label")

    # Transform
    X_train, y_train = pre.transform(train_df, label_column="label")
    X_test, y_test = pre.transform(test_df, label_column="label")

    # Train model
    model = RandomForestClassifier(
        n_estimators=100, random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    print("\n📊 Classification Report:\n")
    print(classification_report(y_test, y_pred))
    print("✅ Accuracy:", accuracy_score(y_test, y_pred))

    # Save artifacts
    joblib.dump(model, "models/trained_model.pkl")
    joblib.dump(pre, "models/preprocessor.pkl")
    print("\n💾 Model + Preprocessor saved in models/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data", type=str, default="datasets/traffic_dataset.csv",
        help="Path to CSV dataset"
    )
    args = parser.parse_args()
    main(args)
