from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Application, StatusHistory
from .serializers import (
    ApplicationSerializer,
    RegisterSerializer,
    StatusHistorySerializer,
)


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_fields = ["status"]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        StatusHistory.objects.create(
            application=instance,
            old_status="",
            new_status=instance.status,
        )

    def perform_update(self, serializer):
        old_status = self.get_object().status
        instance = serializer.save()
        if instance.status != old_status:
            StatusHistory.objects.create(
                application=instance,
                old_status=old_status,
                new_status=instance.status,
            )

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        application = self.get_object()
        history = application.status_history.all()
        serializer = StatusHistorySerializer(history, many=True)
        return Response(serializer.data)
