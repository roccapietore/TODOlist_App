from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import User
from goals.models import GoalComment, Goal, GoalCategory, Board, BoardParticipant


class TestComments(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='User', password='po324ure11')
        self.board = Board.objects.create(title='Title')
        self.category = GoalCategory.objects.create(title='Category', user=self.user, board=self.board)
        self.goal = Goal.objects.create(title='Goal_title', category=self.category,
                                        status=1, priority=1, user=self.user)
        self.comment = GoalComment.objects.create(text='Comment_text', goal=self.goal, user=self.user)
        self.participant = BoardParticipant.objects.create(board=self.board, user=self.user, role=1)

    def tearDown(self):
        self.client.logout()
        GoalComment.objects.all().delete()
        Goal.objects.all().delete()
        GoalCategory.objects.all().delete()
        BoardParticipant.objects.all().delete()
        Board.objects.all().delete()
        User.objects.all().delete()

    # def test_auth_req_comment(self):
    #     url = reverse('comment_create')
    #     response = self.client.post(url, {'title': 'new_one', 'category': self.category.pk})
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment(self):
        url = reverse(viewname='comment_create')
        self.client.force_login(self.user)
        response = self.client.post(url, {'text': 'new_one', 'goal': self.goal.pk, 'user': self.user.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_json = response.json()
        self.assertEqual(resp_json['text'], 'new_one')

    def test_comment_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='comment_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data is not None)

    def test_get_comment_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='comment_id', kwargs={'pk': self.comment.pk}))
        resp_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_json['text'], 'Comment_text')

    def test_get_404_comment_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='comment_id', kwargs={'pk': 10000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partially_update_comment(self):
        self.client.force_login(self.user)
        response = self.client.patch(reverse(viewname='comment_id', kwargs={'pk': self.comment.pk}),
                                     {'text': 'New_comment_text', 'username': self.user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['text'], 'New_comment_text')

    def test_update_comment(self):
        self.client.force_login(self.user)
        response = self.client.put(reverse(viewname='comment_id', kwargs={'pk': self.comment.pk}),
                                   {'text': 'New_comment_text', 'username': self.user.username, 'goal': self.goal.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['text'], 'New_comment_text')

    def test_delete_comment(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse(viewname='comment_id', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
