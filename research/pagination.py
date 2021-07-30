from rest_framework.pagination import PageNumberPagination


class HomePagination(PageNumberPagination):
    page_size = 24
    page_query_param = "page"
    max_page_size = 30
    page_size_query_param = "page_size"


class ListPagination(PageNumberPagination):
    page_size = 12
    page_query_param = "page"
    max_page_size = 30
    page_size_query_param = "page_size"


class NoticePagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    max_page_size = 20
    page_size_query_param = "page_size"


class AskPagination(PageNumberPagination):
    page_size = 25
    page_query_param = "page"
    max_page_size = 50
    page_size_query_param = "page_size"
