from rest_framework.pagination import PageNumberPagination

class FilePageNumberPagination(PageNumberPagination):
    page_size = 20