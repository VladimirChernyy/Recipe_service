from rest_framework.pagination import PageNumberPagination

from foodgram.constants import CustomPaginatorPageSize


class CustomPagination(PageNumberPagination):
    page_size = CustomPaginatorPageSize.PAGE_SIZE
    page_size_query_param = 'limit'
