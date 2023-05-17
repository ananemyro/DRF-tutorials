from rest_framework.test import APIClient
from . import base_test


class UserLoginTestCase(base_test.NewUserTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_user_login(self):
        client = APIClient()
        result = client.post('/login/', {"email": self.email, "password": self.password}, format="json")
        self.assertEquals(result.status_code, 200)
        self.assertTrue("access" in result.json())
        self.assertTrue("refresh" in result.json())

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()
