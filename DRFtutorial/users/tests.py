from .base_test import UserTestCase
from rest_framework.test import APIClient
from rest_framework import status


class UserLoginTest(UserTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_user_login(self):
        client = APIClient()
        result = client.post("/login", {"email": self.email, "password": self.password}, format="json")
        self.assertEquals(result.status_code, 200)
        self.assertTrue("access" in result.json())
        self.assertTrue("refresh" in result.json())

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()


class LoginTokenVerifyRefreshTest(UserTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_user_login_token_verify(self):
        client = APIClient()
        login_response = client.post("/login", {"email": self.email, "password": self.password}, format="json")
        token_verify_response = client.post("/verify-token", {"token": login_response.json()["access"]}, format="json")
        self.assertEquals(token_verify_response.status_code, 200)

    def test_user_refresh_token(self):
        client = APIClient()
        login_response = client.post("/login", {"email": self.email, "password": self.password}, format="json")
        refresh_response = client.post("/refresh-token", {"refresh": login_response.json()["refresh"]}, format="json")
        self.assertEqual(refresh_response.status_code, 200)

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()


class UserProfileViewSetTest(UserTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_list_user_profiles(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/profiles/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/profiles/{self.user.id}/")
        self.assertEqual(response.status_code, 200)

    def test_create_user_profile(self):
        data = {"email": "test@bell.ca", "name": "test", "password": "test"}
        response = self.client.post("/profiles/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_update_user_profile(self):
        data = {"email": "updated@bell.ca"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/profiles/{self.user.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@bell.ca")

    def test_delete_user_profile(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/profiles/{self.user_to_delete.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self) -> None:
        self.client.logout()
        self.client = None
        super().tearDown()
