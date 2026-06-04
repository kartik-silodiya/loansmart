# LoanSmart

LoanSmart is a beginner-friendly Django 4.2 web app that predicts whether a loan application is likely to be approved using a Random Forest Classifier trained on synthetic Indian loan data.

## Features

- Loan eligibility form with income, credit history, dependents, EMIs, and loan details
- Random Forest prediction with approval/rejection confidence
- Personalized improvement tips
- Prediction history stored in SQLite
- Bootstrap 5 responsive UI
- Management command to retrain the model

## Setup

```bash
cd loansmart
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py train_model
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Retrain The ML Model

```bash
python manage.py train_model
```

This command generates 1000 synthetic rows, trains a Random Forest Classifier, and saves it to:

```text
loan_app/ml/loan_model.pkl
```

## Notes

- Currency is shown in Indian Rupees (₹).
- The model is trained on dummy data and is intended for learning/demo purposes only.
- SQLite is used as the default database.
