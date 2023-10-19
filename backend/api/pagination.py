from rest_framework.pagination import PageNumberPagination

from foodgram.constants import CustomPaginator


class CustomPagination(PageNumberPagination):
    page_size = CustomPaginator.PAGE_SIZE.value
    page_size_query_param = 'limit'
