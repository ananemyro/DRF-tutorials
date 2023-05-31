from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Skill, Teacher, Tutorial


class TutorialTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(name="test", email="test@bell.ca", password="test")
        self.admin_user = get_user_model().objects.create(
            name="admin", email="admin@bell.ca", password="admin", is_staff=True, is_superuser=True
        )
        self.skill = Skill.objects.create(name="QA", level="Beginner")
        self.teacher = Teacher.objects.create(first_name="John", last_name="Doe")
        self.tutorial = Tutorial.objects.create(title="Test tutorial", description="Test Description", published=False)
        self.tutorial1 = Tutorial.objects.create(
            title="Test tutorial 1", description="Test Description 1", published=True
        )
        self.tutorial2 = Tutorial.objects.create(
            title="Test tutorial 2", description="Test Description 2", published=False
        )

    def tearDown(self):
        self.user.delete()
        self.admin_user.delete()
        self.skill.delete()
        self.teacher.delete()
        self.tutorial.delete()
        self.tutorial1.delete()
        self.tutorial2.delete()
