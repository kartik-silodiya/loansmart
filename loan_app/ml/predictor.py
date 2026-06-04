from pathlib import Path

import joblib
import pandas as pd
from django.core.management import call_command

MODEL_PATH = Path(__file__).resolve().parent / "loan_model.pkl"

FEATURE_COLUMNS = [
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

_MODEL = None


def get_model():
    """Load the trained model once and reuse it for every request."""
    global _MODEL
    if _MODEL is None:
        if not MODEL_PATH.exists():
            # Helpful for first-time users: create the demo model automatically.
            call_command("train_model", verbosity=0)
        _MODEL = joblib.load(MODEL_PATH)
    return _MODEL


def application_to_dataframe(application):
    """Convert a Django model instance into the one-row DataFrame expected by sklearn."""
    return pd.DataFrame(
        [
            {
                "age": application.age,
                "gender": application.gender,
                "monthly_income": application.monthly_income,
                "employment_status": application.employment_status,
                "loan_amount": application.loan_amount,
                "loan_duration": application.loan_duration,
                "credit_history": application.credit_history,
                "dependents": application.dependents,
                "existing_emis": application.existing_emis,
            }
        ],
        columns=FEATURE_COLUMNS,
    )


def build_tips(application):
    """Create three simple suggestions based on the applicant's details."""
    tips = []
    emi_ratio = application.existing_emis / max(application.monthly_income, 1)
    requested_ratio = application.loan_amount / max(application.monthly_income * 12, 1)

    if application.credit_history != "Good":
        tips.append("Improve your credit history by paying dues on time before applying again.")
    if emi_ratio > 0.35:
        tips.append("Reduce existing EMIs to improve your loan eligibility.")
    if requested_ratio > 5:
        tips.append("Consider requesting a smaller loan amount compared with your annual income.")
    if application.employment_status == "Unemployed":
        tips.append("A stable income source can significantly increase approval chances.")
    if application.monthly_income < 30000:
        tips.append("Increasing monthly income or adding a co-applicant may strengthen your profile.")
    if int(application.dependents.replace("+", "")) >= 3:
        tips.append("High dependents can affect repayment capacity, so keep obligations low.")

    default_tips = [
        "Maintain a good credit history to keep approval chances strong.",
        "Keep existing EMIs below 30-35% of your monthly income.",
        "Choose a loan amount and duration that match your repayment capacity.",
    ]

    for tip in default_tips:
        if len(tips) == 3:
            break
        if tip not in tips:
            tips.append(tip)

    return tips[:3]


def predict_loan_eligibility(application):
    """Return prediction label, confidence percentage, and personalized tips."""
    model = get_model()
    input_data = application_to_dataframe(application)
    prediction_value = int(model.predict(input_data)[0])
    probabilities = model.predict_proba(input_data)[0]
    confidence = round(float(probabilities[prediction_value]) * 100, 1)
    prediction = "APPROVED" if prediction_value == 1 else "REJECTED"
    return prediction, confidence, build_tips(application)
