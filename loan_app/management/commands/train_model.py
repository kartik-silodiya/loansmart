from django.core.management.base import BaseCommand

from loan_app.ml.train_model import train_and_save_model


class Command(BaseCommand):
    help = "Generate synthetic loan data and retrain the Random Forest model."

    def handle(self, *args, **options):
        accuracy, path = train_and_save_model()
        self.stdout.write(self.style.SUCCESS(f"Model trained successfully: {path}"))
        self.stdout.write(self.style.SUCCESS(f"Validation accuracy: {accuracy:.2%}"))
