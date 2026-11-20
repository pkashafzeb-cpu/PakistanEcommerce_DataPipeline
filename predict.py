
import argparse
from pathlib import Path

import joblib
import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "decision_tree_pipeline.joblib"

# Raw columns required to generate the model features
REQUIRED_COLUMNS = [
    "created_at",
    "Customer Since",
    "sku",
    "price",
    "qty_ordered",
    "grand_total",
    "category_name_1",
    "discount_amount",
    "payment_method",
]

# Exact feature order used during training
FEATURE_COLUMNS = [
    "sku",
    "price",
    "qty_ordered",
    "grand_total",
    "category_name_1",
    "discount_amount",
    "payment_method",
    "order_year",
    "order_month",
    "customer_year",
    "customer_month",
    "customer_tenure_months",
]


def prepare_features(df):
    """Validate input and reproduce training feature engineering."""

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    data = df[REQUIRED_COLUMNS].copy()

    data["created_at"] = pd.to_datetime(
        data["created_at"], errors="coerce"
    )

    data["Customer Since"] = pd.to_datetime(
        data["Customer Since"], errors="coerce"
    )

    if data["created_at"].isna().any():
        raise ValueError("Some created_at values are missing or invalid.")

    # Extract date components
    data["order_year"] = data["created_at"].dt.year
    data["order_month"] = data["created_at"].dt.month

    data["customer_year"] = data["Customer Since"].dt.year
    data["customer_month"] = data["Customer Since"].dt.month

    # Calculate customer tenure in months
    data["customer_tenure_months"] = (
        (data["created_at"].dt.year - data["Customer Since"].dt.year) * 12
        + (
            data["created_at"].dt.month
            - data["Customer Since"].dt.month
        )
    )

    return data[FEATURE_COLUMNS]


def main():
    parser = argparse.ArgumentParser(
        description="Predict e-commerce order status."
    )

    parser.add_argument(
        "input_csv",
        help="Path to CSV containing new e-commerce records."
    )

    parser.add_argument(
        "--output",
        default="outputs/predictions.csv",
        help="Path for saving predictions."
    )

    args = parser.parse_args()

    input_path = Path(args.input_csv)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    print("Loading input data...")
    df = pd.read_csv(input_path)

    print("Preparing features...")
    X = prepare_features(df)

    print("Loading trained model...")
    pipeline = joblib.load(MODEL_PATH)

    print("Generating predictions...")
    predictions = pipeline.predict(X)

    # Save original records with predicted status
    results = df.copy()
    results["predicted_status"] = predictions

    output_path = (
        output_path
        if output_path.is_absolute()
        else BASE_DIR / output_path
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)

    print(f"\nPredictions completed: {len(predictions)} records")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()
