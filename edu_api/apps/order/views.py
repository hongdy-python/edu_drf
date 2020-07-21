from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView

from order.models import Order
from order.serializer import OrederModelSerializer



class OrderAPIView(CreateAPIView):
    queryset = Order.objects.filter(is_delete=False,is_show=True)
    serializer_class = OrederModelSerializer
