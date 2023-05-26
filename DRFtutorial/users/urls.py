from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router = DefaultRouter()
router.register('profiles', views.UserProfileViewSet)

urlpatterns = [
    re_path(r'', include(router.urls)),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token', TokenVerifyView.as_view(), name='token_verify'),
]
