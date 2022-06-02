from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import User
from goals.models import Board, Goal, GoalCategory, BoardParticipant


class TestGoals(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='User', password='po324ure11')
        self.board = Board.objects.create(title='Board_title')
        self.category = GoalCategory.objects.create(title='Category', user=self.user, board=self.board)
        self.goal = Goal.objects.create(title='Goal_title', category=self.category,
                                        status=1, priority=1, user=self.user)
        self.participant = BoardParticipant.objects.create(board=self.board, user=self.user, role=1)

    def tearDown(self):
        self.client.logout()
        Goal.objects.all().delete()
        GoalCategory.objects.all().delete()
        BoardParticipant.objects.all().delete()
        Board.objects.all().delete()
        User.objects.all().delete()

    # def test_auth_req_goal(self):
    #     url = reverse('goal_create')
    #     response = self.client.post(url, {'title': 'new_one', 'category': self.category.pk})
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_goal(self):
        url = reverse(viewname='goal_create')
        self.client.force_login(self.user)
        response = self.client.post(url, {'title': 'new_one', 'category': self.category.pk,
                                          'status': 1, 'priority': 1, 'user': self.user.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_json = response.json()
        self.assertEqual(resp_json['title'], 'new_one')

    def test_goal_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='goal_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data is not None)

    def test_get_goal_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='goal_id', kwargs={'pk': self.goal.pk}))
        resp_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_json['title'], 'Goal_title')

    def test_get_404_goal_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='goal_id', kwargs={'pk': 10000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_goal(self):
        self.client.force_login(self.user)
        response = self.client.patch(reverse(viewname='goal_id', kwargs={'pk': self.goal.pk}),
                                     {'title': 'New_goal_title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['title'], 'New_goal_title')

    def test_delete_goal(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse(viewname='goal_id', kwargs={'pk': self.goal.pk}))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
