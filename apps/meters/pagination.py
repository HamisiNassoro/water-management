from rest_framework.pagination import PageNumberPagination


class MeterManagementPagination(PageNumberPagination):
    page_size = 3
