from django.urls import re_path, include, path
from .views import *
from .views import (
    TutorialListViewGenericsMixins,
    TutorialListPublishedViewGenericsMixins,
    TeacherListViewGenericsMixins,
    SkillListViewGenericsMixins,
)


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
    re_path(r'^tutorials$', TutorialListViewGenericsMixins.as_view({'get': 'list', 'post': 'create', 'delete': 'delete'}), name='tutorial_list'),
    re_path(r'^tutorials/(?P<id>[0-9]+)$', TutorialDetailViewGenericsMixins.as_view(),
            name='tutorial_detail'),
    re_path(r'^tutorials/published$', TutorialListPublishedViewGenericsMixins.as_view(),
            name='tutorial_list_published'),
    re_path(r'^teachers$', TeacherListViewGenericsMixins.as_view({'get': 'list', 'post': 'create', 'delete': 'delete'})),
    re_path(r'^teachers/(?P<id>[0-9]+)$', TeacherDetailViewGenericsMixins.as_view()),
    re_path(r'^skills$', SkillListViewGenericsMixins.as_view({'get': 'list', 'post': 'create', 'delete': 'delete'})),
    re_path(r'^skills/(?P<id>[0-9]+)$', SkillDetailViewGenericsMixins.as_view()),
]
