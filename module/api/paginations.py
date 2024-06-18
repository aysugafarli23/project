from rest_framework.pagination import PageNumberPagination

class ModulePagination(PageNumberPagination):
    page_size = 5