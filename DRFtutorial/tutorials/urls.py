from django.urls import re_path, path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'skills', SkillListView)
router.register(r'teachers', TeacherListView)
router.register(r'tutorials', TutorialListView)

# IN USE

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^tutorials/(?P<id>[0-9]+)$', TutorialDetailView.as_view(), name='tutorial_detail'),
    re_path(r'^tutorials/published$', TutorialListPublishedView.as_view(), name='tutorial_list_published'),
    re_path(r'^teachers/(?P<id>[0-9]+)$', TeacherDetailView.as_view()),
    re_path(r'^skills/(?P<id>[0-9]+)$', SkillDetailView.as_view()),
]


"""

# FUNCTION-BASED VIEWS

urlpatterns = [
    re_path(r'^api/tutorials$', tutorial_list, name='tutorial_list'),
    re_path(r'^api/tutorials/(?P<pk>[0-9]+)$', tutorial_detail, name='tutorial_detail'),  # pk: django-specific, 'primary key'
    re_path(r'^api/tutorials/published$', tutorial_list_published, name='tutorial_list_published'),
]

# CLASS-BASED VIEWS (GENERICS)

urlpatterns = [
    re_path(r'^api/tutorials$', views.TutorialListViewGenerics.as_view()),
    re_path(r'^api/tutorials/(?P<pk>[0-9]+)$', views.TutorialDetailViewGenerics.as_view()),
    re_path(r'^api/tutorials/published$', views.TutorialListPublishedViewGenerics.as_view()),
]

# VIEWSETS

router = routers.DefaultRouter()
router.register(r'tutorials', TutorialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

"""
