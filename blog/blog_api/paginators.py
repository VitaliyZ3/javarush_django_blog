from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ArticlePaginator(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(data)