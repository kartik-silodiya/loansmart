from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoanApplicationForm
from .ml.predictor import predict_loan_eligibility
from .models import LoanApplication


def application_form(request):
    """Display the loan form and save a prediction after submission."""
    if request.method == "POST":
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            prediction, confidence, tips = predict_loan_eligibility(application)
            application.prediction = prediction
            application.confidence = confidence
            application.tips = tips
            application.save()
            messages.success(request, "Your loan eligibility prediction is ready.")
            return redirect("loan_app:result", pk=application.pk)
    else:
        form = LoanApplicationForm()

    return render(request, "form.html", {"form": form})


def result(request, pk):
    """Show the prediction result for a saved application."""
    application = get_object_or_404(LoanApplication, pk=pk)
    return render(request, "result.html", {"application": application})


def history(request):
    """Show previous predictions stored in the database."""
    applications = LoanApplication.objects.all()
    return render(request, "history.html", {"applications": applications})
