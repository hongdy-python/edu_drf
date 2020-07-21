from django.urls import path

from payments import views

urlpatterns=[
    path('result/',views.AliPayAPIView.as_view()),
    path('results/',views.AliPayResultAPIView.as_view()),
]