from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import User
from goals.models import Board, GoalCategory, BoardParticipant, Goal, GoalComment


class TestUserLogin(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='Solder', password='po324ure11')
        self.user_2 = User.objects.create(username='Poly', password='sjnfUu30kl0')
        self.board = Board.objects.create(title='Title1')
        self.category = GoalCategory.objects.create(title='Category', user=self.user, board=self.board)
        self.new_participant = BoardParticipant.objects.create(board=self.board, user=self.user, role=1)
        self.goal = Goal.objects.create(title='Goal_title', category=self.category,
                                        status=1, priority=1, user=self.user)
        self.comment = GoalComment.objects.create(text='Comment_text', goal=self.goal, user=self.user)
        self.participant = BoardParticipant.objects.create(board=self.board, user=self.user_2, role=1)

    def tearDown(self):
        self.client.logout()
        GoalComment.objects.all().delete()
        Goal.objects.all().delete()
        GoalCategory.objects.all().delete()
        BoardParticipant.objects.all().delete()
        Board.objects.all().delete()
        User.objects.all().delete()

    def test_auth_req_user(self):
        response = self.client.patch(reverse(viewname='profile'), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_user_login(self):
    #     response = self.client.post('login', {"username": self.user.username,
    #                                           "password": self.user.password,
    #                                           })
    #     resp_json = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(resp_json, {"username": 'User', "password": 'po324ure11'})
    #
    # def test_signup(self):
    #     response = self.client.post('signup', {'username': "newuser",
    #                                            "password": "passUUik39kl",
    #                                            "password_repeat": "passUUik39kl",
    #                                            })
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     resp_json = response.json()
    #     self.assertEqual(resp_json["username"], 'newuser')
    #     self.assertEqual(resp_json["password"], 'passUUik39kl')

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



