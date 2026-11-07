from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from restaurant.views import BookingViewSet, MenuItemViewSet

router = DefaultRouter()
router.register("menu/items", MenuItemViewSet, basename="menu-item")
router.register("booking/tables", BookingViewSet, basename="booking")
index = TemplateView.as_view(template_name="restaurant/index.html")

urlpatterns = [
    path("", index, name="home"),
    path("restaurant/", index, name="restaurant"),
    path("restaurant/", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("api-token-auth/", obtain_auth_token, name="api-token"),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]
