from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

MODEL_PATH = Path(__file__).resolve().parent / "loan_model.pkl"


def generate_synthetic_data(rows=1000, random_state=42):
    """Generate realistic dummy data for learning/demo predictions."""
    rng = np.random.default_rng(random_state)

    data = pd.DataFrame(
        {
            "age": rng.integers(21, 66, rows),
            "gender": rng.choice(["Male", "Female"], rows),
            "monthly_income": rng.integers(12000, 180000, rows),
            "employment_status": rng.choice(
                ["Salaried", "Self-Employed", "Unemployed"],
                rows,
                p=[0.58, 0.32, 0.10],
            ),
            "loan_amount": rng.integers(50000, 3000000, rows),
            "loan_duration": rng.choice([12, 24, 36, 60], rows),
            "credit_history": rng.choice(
                ["Good", "Bad", "No History"],
                rows,
                p=[0.62, 0.20, 0.18],
            ),
            "dependents": rng.choice(["0", "1", "2", "3+"], rows, p=[0.35, 0.28, 0.22, 0.15]),
            "existing_emis": rng.integers(0, 65000, rows),
        }
    )

    annual_income = data["monthly_income"] * 12
    emi_ratio = data["existing_emis"] / data["monthly_income"].clip(lower=1)
    loan_to_income = data["loan_amount"] / annual_income.clip(lower=1)

    # Start with a score and adjust it using common lending signals.
    score = np.zeros(rows)
    score += np.where(data["monthly_income"] >= 75000, 2.0, 0)
    score += np.where(data["monthly_income"].between(35000, 74999), 1.0, 0)
    score += np.where(data["credit_history"] == "Good", 2.4, 0)
    score -= np.where(data["credit_history"] == "Bad", 2.2, 0)
    score -= np.where(data["credit_history"] == "No History", 0.7, 0)
    score += np.where(data["employment_status"] == "Salaried", 1.0, 0)
    score += np.where(data["employment_status"] == "Self-Employed", 0.4, 0)
    score -= np.where(data["employment_status"] == "Unemployed", 2.3, 0)
    score -= np.where(emi_ratio > 0.40, 2.0, 0)
    score -= np.where(emi_ratio.between(0.25, 0.40), 0.8, 0)
    score -= np.where(loan_to_income > 5.0, 1.6, 0)
    score -= np.where(data["dependents"] == "3+", 0.7, 0)
    score -= np.where(data["age"] < 23, 0.3, 0)
    score += rng.normal(0, 0.7, rows)

    data["approved"] = (score > 1.2).astype(int)
    return data


def train_and_save_model(output_path=MODEL_PATH):
    """Train the Random Forest model and save it with joblib."""
    data = generate_synthetic_data()
    feature_columns = [
        "age",
        "gender",
        "monthly_income",
        "employment_status",
        "loan_amount",
        "loan_duration",
        "credit_history",
        "dependents",
        "existing_emis",
    ]
    X = data[feature_columns]
    y = data["approved"]

    categorical_columns = ["gender", "employment_status", "credit_history", "dependents"]
    numeric_columns = [
        "age",
        "monthly_income",
        "loan_amount",
        "loan_duration",
        "existing_emis",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
            ("numeric", "passthrough", numeric_columns),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=160,
                    random_state=42,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return accuracy, output_path


if __name__ == "__main__":
    score, path = train_and_save_model()
    print(f"Model saved to {path} with test accuracy: {score:.2%}")
