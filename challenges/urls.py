from django.urls import path
from .views import DetectingChange, SeasonProblem, CustomOrderStatus

urlpatterns = [
    path('detecting-change', DetectingChange.as_view(), name="detecting-change"),
    path('season-problem', SeasonProblem.as_view(), name="season-problem"),
    path('customer-order-status', CustomOrderStatus.as_view(), name="customer-order-status"),
]
