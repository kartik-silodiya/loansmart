# Generated manually for the LoanSmart demo app.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LoanApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=100)),
                ("age", models.PositiveIntegerField()),
                ("gender", models.CharField(choices=[("Male", "Male"), ("Female", "Female")], max_length=10)),
                ("monthly_income", models.PositiveIntegerField(help_text="Monthly income in ₹")),
                (
                    "employment_status",
                    models.CharField(
                        choices=[
                            ("Salaried", "Salaried"),
                            ("Self-Employed", "Self-Employed"),
                            ("Unemployed", "Unemployed"),
                        ],
                        max_length=20,
                    ),
                ),
                ("loan_amount", models.PositiveIntegerField(help_text="Requested loan amount in ₹")),
                (
                    "loan_duration",
                    models.PositiveIntegerField(
                        choices=[(12, "12 months"), (24, "24 months"), (36, "36 months"), (60, "60 months")]
                    ),
                ),
                (
                    "credit_history",
                    models.CharField(
                        choices=[("Good", "Good"), ("Bad", "Bad"), ("No History", "No History")],
                        max_length=20,
                    ),
                ),
                (
                    "dependents",
                    models.CharField(choices=[("0", "0"), ("1", "1"), ("2", "2"), ("3+", "3+")], max_length=2),
                ),
                ("existing_emis", models.PositiveIntegerField(default=0, help_text="Existing EMIs per month in ₹")),
                (
                    "prediction",
                    models.CharField(
                        blank=True,
                        choices=[("APPROVED", "Approved"), ("REJECTED", "Rejected")],
                        max_length=10,
                    ),
                ),
                ("confidence", models.FloatField(default=0)),
                ("tips", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
