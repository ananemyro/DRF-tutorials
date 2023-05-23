from django.urls import re_path, include
from .views import *
from . import views


"""
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tutorials', TutorialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""

"""
# function-based views

urlpatterns = [
    re_path(r'^api/tutorials$', tutorial_list, name='tutorial_list'),
    re_path(r'^api/tutorials/(?P<pk>[0-9]+)$', tutorial_detail, name='tutorial_detail'),  # pk: django-specific, 'primary key'
    re_path(r'^api/tutorials/published$', tutorial_list_published, name='tutorial_list_published'),
]
"""

"""
# class-based views + generics

urlpatterns = [
    re_path(r'^api/tutorials$', views.TutorialListViewGenerics.as_view()),
    re_path(r'^api/tutorials/(?P<pk>[0-9]+)$', views.TutorialDetailViewGenerics.as_view()),
    re_path(r'^api/tutorials/published$', views.TutorialListPublishedViewGenerics.as_view()),
]
"""

# class-based views + generics + mixins (IN USE)

urlpatterns = [
    re_path(r'^tutorials$', views.TutorialListViewGenericsMixins.as_view(), name='tutorial_list'),
    re_path(r'^tutorials/(?P<id>[0-9]+)$', views.TutorialDetailViewGenericsMixins.as_view(),
            name='tutorial_detail'),
    re_path(r'^tutorials/published$', views.TutorialListPublishedViewGenericsMixins.as_view(),
            name='tutorial_list_published'),
    re_path(r'^teachers$', views.TeachersListViewGenericsMixins.as_view(), name='teachers_list'),
    re_path(r'^skills$', views.SkillsListViewGenericsMixins.as_view(), name='skills_list'),
]
