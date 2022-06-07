from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import User
from goals.models import Board, GoalCategory, BoardParticipant, Goal, GoalComment


class TestUserLogin(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='Solder')
        self._user_password = 'po324ure11'
        self.user.set_password(self._user_password)
        self.user.save(update_fields=['password'])

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()

    def test_auth_req_user(self):
        response = self.client.patch(reverse(viewname='profile'), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login(self):
        response = self.client.post('login', {"username": self.user.username,
                                              "password": self._user_password,
                                              })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.json(),
            {
                'id': self.user.id,
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email
            })

    def test_signup(self):
        response = self.client.post('signup', {"username": self.user.username,
                                               "password": self._user_password,
                                               "password_repeat": self._user_password,
                                               })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_json = response.json()
        self.assertEqual(resp_json["username"], 'Solder')


    # def test_get_user(self):
    #     self.client.force_login(self.user)
    #     response = self.client.get('profile')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(response.data is not None)

    # def test_partially_update_user(self):
    #     self.client.force_login(self.user)
    #     response = self.client.patch('profile', {'username': self.user.username, 'first_name': 'New_firstname'}),
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     resp_json = response.json()
    #     self.assertEqual(resp_json['first_name'], 'New_firstname')
    #
    # def test_delete_user(self):
    #     self.client.force_login(self.user)
    #     response = self.client.delete('profile')
    #     self.assertEqual(response.data, None)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_partially_update_user_password(self):
    #     self.client.force_login(self.user)
    #     response = self.client.patch('profile', {'old_password': self.user.password, 'new_password': 'ne32nkeoo28'}),
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     resp_json = response.json()
    #     self.assertEqual(resp_json['new_password'], 'ne32nkeoo28')
    #
    # def test_update_user_password(self):
    #     self.client.force_login(self.user)
    #     response = self.client.put('profile', {'old_password': self.user.password, 'new_password': 'ne32nkeoo28'}),
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     resp_json = response.json()
    #     self.assertEqual(resp_json['new_password'], 'ne32nkeoo28')
