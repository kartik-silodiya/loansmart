from django import forms

from .models import LoanApplication


class LoanApplicationForm(forms.ModelForm):
    """Bootstrap-friendly form for collecting loan details."""

    class Meta:
        model = LoanApplication
        fields = [
            "full_name",
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
        labels = {
            "monthly_income": "Monthly Income (₹)",
            "loan_amount": "Loan Amount Requested (₹)",
            "loan_duration": "Loan Duration",
            "existing_emis": "Existing EMIs per month (₹)",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Enter your full name"}),
            "age": forms.NumberInput(attrs={"min": 18, "max": 75}),
            "monthly_income": forms.NumberInput(attrs={"min": 0, "step": 1000}),
            "loan_amount": forms.NumberInput(attrs={"min": 10000, "step": 10000}),
            "existing_emis": forms.NumberInput(attrs={"min": 0, "step": 500}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        for name in ["gender", "employment_status", "loan_duration", "credit_history", "dependents"]:
            self.fields[name].widget.attrs["class"] = "form-select"
