from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from rest_framework import status
from .views import TutorialListView, TeacherListView, SkillListView, SkillDetailView, TeacherDetailView, TutorialDetailView, TutorialListPublishedView
from .models import Tutorial, Teacher, Skill
from .serializers import TutorialSerializer, SkillSerializer, TeacherSerializer, TeacherPublicSerializer


class SkillListViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SkillListView.as_view({'get': 'list', 'post': 'create', 'delete': 'delete_all'})
        self.user = get_user_model().objects.create(name='test', email='test@bell.ca', password="test")
        self.skill = Skill.objects.create(name='QA', level='Beginner')

    def tearDown(self):
        self.user.delete()
        self.skill.delete()

    def test_list_skills(self):
        request = self.factory.get('/skills/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_create_skill(self):
        request = self.factory.post('/skills/', {'name': 'QA', 'level': 'Intermediate'})
        force_authenticate(request, user=self.user)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_delete_skill_list(self):
        request = self.factory.delete('/skills/')
        force_authenticate(request, user=self.user)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Skill.objects.count(), 0)


class TutorialListViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = TutorialListView.as_view({'get': 'list', 'post': 'create', 'delete': 'delete_all'})
        self.user = get_user_model().objects.create_user(name='test', email='test@bell.ca', password='test')
        self.tutorial = Tutorial.objects.create(
            title='Test tutorial',
            description='Test Description',
            published=False,
            teacher=None
        )

    def tearDown(self):
        self.user.delete()
        self.tutorial.delete()

    def test_list_authenticated(self):
        url = '/tutorials/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_unauthenticated(self):
        url = '/tutorials/'
        request = self.factory.get(url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_unauthenticated(self):
        url = '/tutorials/'
        request_data = {
            'title': 'New Tutorial',
            'description': 'New Description',
            'published': True
        }
        request = self.factory.post(url, data=request_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_authenticated(self):
        url = '/tutorials/'
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tutorial.objects.count(), 0)

    def test_destroy_unauthenticated(self):
        url = '/tutorials/'
        request = self.factory.delete(url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TeacherListViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = TeacherListView.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})
        self.user = get_user_model().objects.create_user(name='test', email='test@bell.ca', password="test")
        self.admin_user = get_user_model().objects.create_superuser(
            name='admin',
            email='admin@bell.ca',
            password="admin"
        )
        self.teacher = Teacher.objects.create(
            first_name='John',
            last_name='Doe'
        )

    def tearDown(self):
        self.user.delete()
        self.admin_user.delete()
        self.teacher.delete()

    def test_list_authenticated(self):
        request = self.factory.get('/teachers/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_unauthenticated(self):
        request = self.factory.get('/teachers/')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_unauthenticated(self):
        request_data = {
            'first_name': 'Jane',
            'last_name': 'Eyre'
        }
        request = self.factory.post('/teachers/', data=request_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_authenticated(self):
        request = self.factory.delete('/teachers/')
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Teacher.objects.count(), 0)

    def test_destroy_unauthenticated(self):
        request = self.factory.delete('/teachers/')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

'''
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

'''
