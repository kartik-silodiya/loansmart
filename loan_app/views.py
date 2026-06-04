import json

from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDate
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


def dashboard(request):
    """Show dashboard with stats and charts."""
    total = LoanApplication.objects.count()
    approved = LoanApplication.objects.filter(prediction="APPROVED").count()
    rejected = LoanApplication.objects.filter(prediction="REJECTED").count()
    approval_rate = round((approved / total * 100), 1) if total > 0 else 0

    employment_data = (
        LoanApplication.objects
        .values("employment_status")
        .annotate(count=Count("id"))
        .order_by("employment_status")
    )

    daily_data = (
        LoanApplication.objects
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    context = {
        "total": total,
        "approved": approved,
        "rejected": rejected,
        "approval_rate": approval_rate,
        "employment_labels_json": json.dumps([e["employment_status"] for e in employment_data]),
        "employment_counts_json": json.dumps([e["count"] for e in employment_data]),
        "daily_labels_json": json.dumps([str(d["date"]) for d in daily_data]),
        "daily_counts_json": json.dumps([d["count"] for d in daily_data]),
    }
    return render(request, "dashboard.html", context)