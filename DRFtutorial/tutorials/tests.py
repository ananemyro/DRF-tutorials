from django.test import TestCase, Client
from django.urls import reverse
from .models import Tutorial
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .serializers import TutorialSerializer
from django.contrib.auth import get_user_model


# class-based views


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
# function-based views


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
'''
