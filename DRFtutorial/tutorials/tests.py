from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from rest_framework import status
from .views import (
    TutorialListView,
    TeacherListView,
    SkillListView,
    SkillDetailView,
    TeacherDetailView,
    TutorialDetailView,
    TutorialListPublishedView,
)
from .models import Tutorial, Teacher, Skill
from .serializers import TutorialSerializer
from .base_test import TutorialTestCase


class SkillListViewTestCase(TutorialTestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.view = SkillListView.as_view({"get": "list", "post": "create", "delete": "delete_all"})

    def tearDown(self):
        super().tearDown()

    def test_list_skills_authenticated(self):
        request = self.factory.get("/skills/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_list_skills_unauthenticated(self):
        request = self.factory.get("/skills/")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_create_skill_authenticated(self):
        request = self.factory.post("/skills/", {"name": "QA", "level": "Intermediate"})
        force_authenticate(request, user=self.user)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_create_skill_unauthenticated(self):
        request = self.factory.post("/skills/", {"name": "QA", "level": "Intermediate"})
        response = self.view(request)
        self.assertEqual(response.status_code, 401)

    def test_delete_skills_authenticated(self):
        request = self.factory.delete("/skills/")
        force_authenticate(request, user=self.admin_user)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 204)

    def test_delete_skills_unauthenticated(self):
        request = self.factory.delete("/skills/")
        response = self.view(request)
        self.assertEqual(response.status_code, 401)


class TeacherListViewTestCase(TutorialTestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.view = TeacherListView.as_view({"get": "list", "post": "create", "delete": "destroy"})

    def tearDown(self):
        super().tearDown()

    def test_list_teachers_authenticated(self):
        request = self.factory.get("/teachers/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_teachers_unauthenticated(self):
        request = self.factory.get("/teachers/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_teacher_authenticated(self):
        request_data = {"first_name": "Jane", "last_name": "Eyre"}
        request = self.factory.post("/teachers/", data=request_data)
        request.POST = request.POST.copy()
        request.POST.update(request_data)
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_teacher_unauthenticated(self):
        request_data = {"first_name": "Jane", "last_name": "Eyre"}
        request = self.factory.post("/teachers/", data=request_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_teachers_authenticated(self):
        request = self.factory.delete("/teachers/")
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_teachers_unauthenticated(self):
        request = self.factory.delete("/teachers/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TutorialListViewTestCase(TutorialTestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.view = TutorialListView.as_view({"get": "list", "post": "create", "delete": "delete_all"})

    def tearDown(self):
        super().tearDown()

    def test_list_tutorials_authenticated(self):
        url = "/tutorials/"
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_tutorials_unauthenticated(self):
        url = "/tutorials/"
        request = self.factory.get(url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tutorial_authenticated(self):
        url = "/tutorials/"
        request_data = {"title": "New Tutorial", "description": "New Description", "published": True}
        request = self.factory.post(url)
        request.POST = request.POST.copy()
        request.POST.update(request_data)
        force_authenticate(request, user=self.user)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tutorial_unauthenticated(self):
        url = "/tutorials/"
        request_data = {"title": "New Tutorial", "description": "New Description", "published": True}
        request = self.factory.post(url, data=request_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_tutorial_authenticated(self):
        request = self.factory.delete("/tutorials/")
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_tutorials_unauthenticated(self):
        url = "/tutorials/"
        request = self.factory.delete(url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TutorialListPublishedViewTestCase(TutorialTestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.view = TutorialListPublishedView.as_view()

    def tearDown(self):
        super().tearDown()

    def test_list_published_tutorials_authenticated(self):
        request = self.factory.get("/tutorials/published/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tutorials = Tutorial.objects.filter(published=True).order_by("id")
        serializer = TutorialSerializer(tutorials, many=True)
        expected_data = list(serializer.data)
        response_data = list(response.data.get("results", []))
        self.assertEqual(expected_data, response_data)

    def test_list_published_tutorials_without_permissions(self):
        response = self.client.get("/tutorials/published")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SkillDetailViewTestCase(TutorialTestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.view = SkillDetailView.as_view()

    def tearDown(self):
        super().tearDown()

    def test_get_skill(self):
        request = self.factory.get(f"/skills/{self.skill.id}/")
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.skill.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_skill(self):
        request = self.factory.put(f"/skills/{self.skill.id}/", {"name": "Updated Skill", "level": "Advanced"})
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.skill.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_skill(self):
        request = self.factory.patch(f"/skills/{self.skill.id}/", {"name": "Modified Skill"})
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.skill.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_skill(self):
        request = self.factory.delete(f"/skills/{self.skill.id}/")
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.skill.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TeacherDetailViewTestCase(TutorialTestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.view = TeacherDetailView.as_view()

    def tearDown(self):
        super().tearDown()

    def test_get_teacher(self):
        request = self.factory.get(f"/teachers/{self.teacher.id}/")
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.teacher.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_teacher(self):
        request = self.factory.put(
            f"/teachers/{self.teacher.id}/",
            {"first_name": "Updated", "last_name": "Teacher", "skills": [self.skill.id]},
        )
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.teacher.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_teacher(self):
        request = self.factory.patch(f"/teachers/{self.teacher.id}/", {"first_name": "Modified"})
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.teacher.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_teacher(self):
        request = self.factory.delete(f"/teachers/{self.teacher.id}/")
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.teacher.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TutorialDetailViewTestCase(TutorialTestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.view = TutorialDetailView.as_view()

    def tearDown(self):
        super().tearDown()

    def test_get_tutorial(self):
        request = self.factory.get(f"/tutorials/{self.tutorial.id}/")
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.tutorial.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_tutorial(self):
        request = self.factory.put(
            f"/tutorials/{self.tutorial.id}/",
            {
                "title": "Updated Tutorial",
                "description": "Updated Description",
                "published": False,
                "teacher": self.teacher.id,
            },
        )
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.tutorial.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_tutorial(self):
        request = self.factory.patch(f"/tutorials/{self.tutorial.id}/", {"title": "Modified Tutorial"})
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.tutorial.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tutorial(self):
        request = self.factory.delete(f"/tutorials/{self.tutorial.id}/")
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.tutorial.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


"""
# FUNCTION-BASED VIEWS


class TutorialListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('tutorial_list')

    def test_tutorial_list_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_tutorial_list_post(self):
        data = {'title': 'Test', 'description': 'This is a test tutorial.', 'published': 'false'}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        tutorial = Tutorial.objects.get(title='Test')
        self.assertEqual(tutorial.description, 'This is a test tutorial.')

    def test_tutorial_list_delete(self):
        tutorial = Tutorial.objects.create(title='Test', description='This is a test tutorial.', published=False)
        response = self.client.delete(reverse('tutorial_detail', kwargs={'pk': tutorial.pk}))
        self.assertEqual(response.status_code, 204)
        
# CLASS-BASED VIEWS


class TutorialListViewGenericsMixinsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('tutorial_list')
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpassword',
        )
        self.client.force_authenticate(user=self.user)

    def test_tutorial_list_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tutorial_list_post(self):
        data = {'title': 'Test', 'description': 'This is a test tutorial.', 'published': 'false'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tutorial = Tutorial.objects.get(title='Test')
        serializer = TutorialSerializer(tutorial)
        self.assertEqual(response.data, serializer.data)

    def test_tutorial_list_delete(self):
        tutorial = Tutorial.objects.create(title='Test', description='This is a test tutorial.', published=False)
        response = self.client.delete(reverse('tutorial_detail', args=[tutorial.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tutorial.objects.filter(id=tutorial.id).exists())

"""
