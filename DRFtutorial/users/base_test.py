from django.test import TestCase
from django.contrib.auth.models import User
from faker import Faker

class NewUserTestCase(TestCase):

    def setUp(self) -> None:
        faker = Faker()
        self.email = faker.email()
        self.username = faker.user_name()
        self.password = faker.password()
        self.user = User.objects.create_user(email=self.email,
                                             username=self.username,
                                             password=self.password)

        def tearDown(self) -> None:
            self.user.delete()
