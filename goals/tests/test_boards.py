from rest_framework import status
from django.urls import reverse
from goals.tests import base_test


class TestBoard(base_test.TestBase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

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
        response = self.client.get(reverse(viewname='board_id', kwargs={'pk': self.board.pk}))
        resp_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_json['title'], 'Title')

    def test_get_404_board_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='board_id', kwargs={'pk': 10000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partially_update_board(self):
        self.client.force_login(self.user)
        response = self.client.patch(reverse(viewname='board_id', kwargs={'pk': self.board.pk}),
                                     {'title': 'New_title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['title'], 'New_title')

    # def test_update_board(self):
    #     self.client.force_login(self.user)
    #     response = self.client.put(reverse(viewname='board_id', kwargs={'pk': self.new_board.pk}),
    #                                {'title': 'New_title', 'is_deleted': False,
    #                                 'participants': {
    #                                     'role': self.new_participant.role,
    #                                     'user': self.user.username}})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     resp_json = response.json()
    #     self.assertEqual(resp_json['title'], 'New_title')

    def test_delete_board(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse(viewname='board_id', kwargs={'pk': self.board.pk}))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
