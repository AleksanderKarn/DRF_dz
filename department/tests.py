from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User(
            email='abc@mail.ru',
        )

        self.user.set_password('abc123')
        self.user.save()

        response = self.client.post(
            '/user/api/token/',
            {'email': 'abc@mail.ru', 'password': 'abc123'}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


    def test_lesson_create(self):
        response = self.client.post(
            '/department/lesson/create/',
            {'name': 'ABC', 'link': 'https://www.youtube.com/watch?v=LxIZIsMB4JQ&ab_channel=%D0%98%D0%B2%D0%B0%D0%BD%D0%92%D0%B8%D0%BA%D1%82%D0%BE%D1%80%D0%BE%D0%B2%D0%B8%D1%87'}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_get_lesson(self):
        self.test_lesson_create()
        response = self.client.get(
            f'/department/lesson/15/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': 1,
                'name': 'ABC',
                'link': 'https://www.youtube.com/watch?v=LxIZIsMB4JQ&ab_channel=%D0%98%D0%B2%D0%B0%D0%BD%D0%92%D0%B8%D0%BA%D1%82%D0%BE%D1%80%D0%BE%D0%B2%D0%B8%D1%87',
                'course': 'null',
                'preview': 'null',
                'owner': 'null'
            }
        )

    def test_lesson_update(self):
        pass

    def test_lesson_delete(self):
        pass