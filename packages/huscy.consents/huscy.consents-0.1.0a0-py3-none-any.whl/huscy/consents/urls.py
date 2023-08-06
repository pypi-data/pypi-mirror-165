from django.urls import path
from huscy.consents import views

urlpatterns = [
    path('', views.ConsentView.as_view(), name="consent-view"),
]
