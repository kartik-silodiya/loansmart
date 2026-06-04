from django.db import models


class LoanApplication(models.Model):
    """Stores each submitted loan application and its prediction result."""

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    EMPLOYMENT_CHOICES = [
        ("Salaried", "Salaried"),
        ("Self-Employed", "Self-Employed"),
        ("Unemployed", "Unemployed"),
    ]

    DURATION_CHOICES = [
        (12, "12 months"),
        (24, "24 months"),
        (36, "36 months"),
        (60, "60 months"),
    ]

    CREDIT_HISTORY_CHOICES = [
        ("Good", "Good"),
        ("Bad", "Bad"),
        ("No History", "No History"),
    ]

    DEPENDENTS_CHOICES = [
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3+", "3+"),
    ]

    PREDICTION_CHOICES = [
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    monthly_income = models.PositiveIntegerField(help_text="Monthly income in ₹")
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES)
    loan_amount = models.PositiveIntegerField(help_text="Requested loan amount in ₹")
    loan_duration = models.PositiveIntegerField(choices=DURATION_CHOICES)
    credit_history = models.CharField(max_length=20, choices=CREDIT_HISTORY_CHOICES)
    dependents = models.CharField(max_length=2, choices=DEPENDENTS_CHOICES)
    existing_emis = models.PositiveIntegerField(default=0, help_text="Existing EMIs per month in ₹")

    prediction = models.CharField(
        max_length=10,
        choices=PREDICTION_CHOICES,
        blank=True,
    )
    confidence = models.FloatField(default=0)
    tips = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.prediction or 'Pending'}"
