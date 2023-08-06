import json

from django.db.models import Q
from django.views.generic import TemplateView
from health_check.views import MainView
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from translate.service.models import Translation
from translate.service.paginations import TranslateClientPagination
from translate.service.serializers import LivelinessCheckSerializer, ReadinessCheckSerializer, TranslationSerializer


class TranslationsAPIView(ListAPIView):
    """
    This view should return a list of translations
    for provided language
    """

    serializer_class = TranslationSerializer
    pagination_class = TranslateClientPagination
    queryset = Translation.objects

    def get(self, request, *args, **kwargs):
        query = Q(language__lang_info=kwargs.get("language"))

        view_names = self.request.GET.getlist("view_name")
        if view_names:
            query &= Q(key__views__contains=view_names)

        occurrences = self.request.GET.getlist("occurrences")
        if occurrences:
            query &= Q(key__occurrences__contains=occurrences)

        snake_keys = self.request.GET.getlist("snake_keys")
        if snake_keys:
            query &= Q(key__snake_name__in=snake_keys)

        serializer = TranslationSerializer(self.paginate_queryset(self.queryset.filter(query)), many=True)
        return Response(serializer.data)


class LivelinessCheckView(GenericAPIView):
    """Liveliness check view."""

    serializer_class = LivelinessCheckSerializer

    def get(self, request, *args, **kwargs):
        """Returns liveliness check response."""
        return Response(self.get_serializer().data, status=status.HTTP_200_OK)


class ReadinessCheckView(MainView, GenericAPIView):
    """Readiness check view."""

    serializer_class = ReadinessCheckSerializer

    def get(self, request, *args, **kwargs):
        """Return readiness check response."""
        request.GET = request.GET.copy()
        request.GET["format"] = "json"

        parent = super().get(request, *args, **kwargs)
        data = json.loads(parent.getvalue())

        return Response(self.get_serializer(data).data, status=parent.status_code)


class HomeView(TemplateView):

    template_name = "index.html"
