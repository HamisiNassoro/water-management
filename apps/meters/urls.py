from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.ListAllMetersAPIView.as_view(), name="all-meters"),
    path(
        "customers/", views.ListCustomersMetersAPIView.as_view(), name="customer-meters"
    ),
    path("create/", views.create_meter_api_view, name="meter-create"),
   path(
        "details/<slug:slug>/",
        views.MeterDetailView.as_view(),
        name="property-details",
    ),
        
    path("update/<slug:slug>/", views.update_meter_api_view, name="update-meter"),
    path("delete/<slug:slug>/", views.delete_meter_api_view, name="delete-meter"),
    path("search/", views.MeterManagementSearchAPIView.as_view(), name="meter-search"),

]