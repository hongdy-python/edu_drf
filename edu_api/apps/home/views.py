from rest_framework.generics import ListAPIView

from home.models import Banner, Nav
from home.serializers import BannerModelSerializer, NavModelSerializer
from edu_api.settings.constants import BANNER_LENGTH, NAV_LENGTH

class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("-orders")

    serializer_class = BannerModelSerializer

class NavListAPIView(ListAPIView):
    # queryset = Nav.objects.filter(is_show=True, is_delete=False).order_by('-orders')[:NAV_LENGTH]
    queryset = Nav.objects.filter(is_show=True, is_delete=False).order_by('-orders')
    serializer_class = NavModelSerializer