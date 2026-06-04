from django.urls import path

from . import views

app_name = "loan_app"

urlpatterns = [
    path("", views.application_form, name="form"),
    path("result/<int:pk>/", views.result, name="result"),
    path("history/", views.history, name="history"),
]
