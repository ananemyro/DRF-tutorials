from rest_framework import viewsets
from .models import UserProfile
from . import serializers
from . import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
