from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import User
from goals.models import Board, BoardParticipant


class TestBoard(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='User', password='po324ure11')
        self.new_board = Board.objects.create(title='Title')
        self.new_participant = BoardParticipant.objects.create(board=self.new_board, user=self.user, role=1)

    def tearDown(self):
        self.client.logout()
        BoardParticipant.objects.all().delete()
        Board.objects.all().delete()
        User.objects.all().delete()

    def test_auth_req(self):
        url = reverse('board_create')
        response = self.client.post(url, {'title': 'board'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_board(self):
        url = reverse('board_create')
        self.client.force_login(self.user)
        response = self.client.post(url, {'title': 'board'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_json = response.json()
        self.assertEqual(resp_json['title'], 'board')
        self.assertEqual(resp_json['is_deleted'], False)

    def test_board_list(self):
        url = reverse('board_list')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data is not None)

    def test_get_board_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='board_id', kwargs={'pk': self.new_board.pk}))
        resp_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_json['title'], 'Title')

    def test_get_404_board_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='board_id', kwargs={'pk': 10000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_board(self):
        self.client.force_login(self.user)
        response = self.client.patch(reverse(viewname='board_id', kwargs={'pk': self.new_board.pk}),
                                     {'title': 'New_title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['title'], 'New_title')

    def test_delete_board(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse(viewname='board_id', kwargs={'pk': self.new_board.pk}))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
