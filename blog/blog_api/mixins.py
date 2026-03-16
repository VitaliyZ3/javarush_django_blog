from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

class ReadAndCreateModelViewSet(RetrieveModelMixin,
                    ListModelMixin,
                    CreateModelMixin,
                    GenericViewSet):
    """ Can create and get single or list of objects"""
    pass