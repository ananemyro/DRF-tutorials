from django.test import TestCase
from django.contrib.auth import get_user_model
from faker import Faker


class NewUserTestCase(TestCase):

    def setUp(self) -> None:
        faker = Faker()
        self.email = faker.email()
        self.username = faker.user_name()
        self.password = faker.password()
        self.user = get_user_model().objects.create_user(email=self.email,
                                                         name=self.username,
                                                         password=self.password)

    def tearDown(self) -> None:
        self.user.delete()
