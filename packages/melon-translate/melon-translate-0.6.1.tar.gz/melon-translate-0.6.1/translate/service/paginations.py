from rest_framework import pagination


class TranslateClientPagination(pagination.PageNumberPagination):
    """TranslateClient Pagination class."""

    page_size = 3000
    page_size_query_param = "page_size"
    max_page_size = 5000
    page_query_param = "page"
