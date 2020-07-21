from django.urls import path

from order import views

urlpatterns = [
    path('getorder/',views.OrderAPIView.as_view())
]