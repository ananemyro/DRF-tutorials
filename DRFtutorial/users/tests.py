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


class LoginTokenVerifyTest(base_test.NewUserTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_user_login_token_verify(self):
        client = APIClient()
        login_response = client.post('/login/', {"email": self.email, "password": self.password}, format="json")
        token_verify_response = client.post('/verify-token/', {"token": login_response.json()['access']}, format="json")
        self.assertEquals(token_verify_response.status_code, 200)

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()

