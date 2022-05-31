from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import User
from goals.models import Board
from goals.serializers import BoardCreateSerializer


class TestBoard(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='user',
            password='po324ure11'
        )

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

    def tearDown(self):
        self.user.delete()



