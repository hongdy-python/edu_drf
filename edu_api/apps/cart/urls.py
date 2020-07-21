from django.urls import path

from cart import views

urlpatterns = [
    path("option/",views.CartViewSet.as_view({"post":"add_cart",
                                              "get":"list_cart",
                                              "patch":"change_select",
                                              "put": "change_expire"})),
    path("option/<str:id>",views.CartViewSet.as_view({'delete':'delete_cart'})),
    path("order/",views.CartViewSet.as_view({'get':'get_select_course'})),
]