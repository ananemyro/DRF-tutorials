import logging
from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer
from .permissions import UpdateOwnProfile
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)

class UserProfileViewSet(viewsets.ModelViewSet):

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().order_by("id")
    authentication_classes = (JWTAuthentication,)
    permission_classes = [UpdateOwnProfile]

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return []
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        logger.info("Listing user profiles...")
        response = super().list(self, request, *args, **kwargs)
        logger.info("Listed successfully.")
        return response

    def perform_create(self, serializer):
        logger.info("Attempting to create a new profile...")
        super().perform_create(serializer)
        logger.info("New profile was created successfully.")

    def perform_update(self, serializer):
        logger.info("Attempting to update the profile...")
        super().perform_update(serializer)
        logger.info("The profile was updated successfully.")

    def perform_destroy(self, instance):
        logger.info("Attempting to delete the profile...")
        super().perform_destroy(instance)
        logger.info("The profile was deleted successfully.")
