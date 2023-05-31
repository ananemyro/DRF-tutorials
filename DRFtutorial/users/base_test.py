from django.test import TestCase
from django.contrib.auth import get_user_model
from faker import Faker


class UserTestCase(TestCase):
    def setUp(self) -> None:
        faker = Faker()
        self.email = faker.email()
        self.username = faker.user_name()
        self.password = faker.password()
        self.user = get_user_model().objects.create_user(email=self.email, name=self.username, password=self.password)
        self.admin_user = get_user_model().objects.create_user(
            email="admin@bell.ca", name="admin", password="admin", is_staff=True, is_superuser=True
        )
        self.user_to_delete = get_user_model().objects.create_user(email="user@bell.ca", name="user", password="user")

    def tearDown(self) -> None:
        self.user.delete()
        self.admin_user.delete()
        self.user_to_delete.delete()
