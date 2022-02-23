from rest_framework import mixins, viewsets
from rest_framework.response import Response


class CustomUpdateModelMixin(object):
    """
    CustomUpdateModelMixin переопределенный только для частичного обновления
    """
    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class ListCreateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Кастомный ViewSet для отображения списка, создания и удаления
    объектов
    """
    pass


class RetrieveListCreateDestroyPartialUpdateViewSet(mixins.RetrieveModelMixin,
                                                    mixins.ListModelMixin,
                                                    mixins.CreateModelMixin,
                                                    mixins.DestroyModelMixin,
                                                    CustomUpdateModelMixin,
                                                    viewsets.GenericViewSet):
    """Кастомный ViewSet для отображения детальной информации, списка,
    создания, удаления и частичного обновления объекта
    """
    pass
