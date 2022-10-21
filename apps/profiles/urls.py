from django.urls import path
from .views import (SiteManagersListAPIView, MeterReadersListAPIView, CustomersListAPIView, GetProfileAPIView, UpdateProfileAPIView)


urlpatterns = [
    path("me/", GetProfileAPIView.as_view(), name="get_profile"),
    path(
        "update/<str:username>/", UpdateProfileAPIView.as_view(), name="update_profile"
    ),
    path("site-managers/all/", SiteManagersListAPIView.as_view(), name="all-site-managers"),
    path("meter-readers/all/", MeterReadersListAPIView.as_view(), name="all-meter-readers"),
    path("customers/all/", CustomersListAPIView.as_view(), name="all-customers"),

]