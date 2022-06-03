from rest_framework import status
from django.urls import reverse
from goals.tests import base_test


class TestComments(base_test.TestBase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    # def test_auth_req_comment(self):
    #     url = reverse(viewname='comment_create')
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
