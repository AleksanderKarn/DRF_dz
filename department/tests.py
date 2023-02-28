from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User


class LessonTestCase(APITestCase):
    test_email = 'abc@mail.ru'
    test_password = 'abc123'

    def setUp(self) -> None:
        self.user = User(
            email=self.test_email,
        )

        self.user.set_password(self.test_password)
        self.user.save()

        response = self.client.post(
            '/user/api/token/',
            {'email': self.test_email, 'password': self.test_password}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_lesson_create(self):
        response = self.client.post(
            '/department/lesson/create/',
            {"name": "ABC", "link": "https://www.youtube.com/watch?v"}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_get_lesson(self):
        self.test_lesson_create()
        response = self.client.get(
            f'/department/lesson/1/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "pk": 1,
                "name": "ABC",
                'preview': None,
                "link": "https://www.youtube.com/watch?v",
                'course_id': None,
                'owner': 1,
            }
        )

    def test_lesson_update(self):
        self.test_lesson_create()
        response = self.client.put(
            f'/department/lesson/update/1/',
            {"name": "CBA", "link": "https://www.youtube.com/watch?"}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "pk": 1,
                "name": "CBA",
                'preview': None,
                "link": "https://www.youtube.com/watch?",
                'course_id': None,
                'owner': 1,
            }
        )

    def test_lesson_delete(self):
        self.test_lesson_create()
        response = self.client.delete(
            f'/department/lesson/delete/1/',
            {"name": "ABC", "link": "https://www.youtube.com/watch?v"}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_course_create(self):
        response = self.client.post(
            '/department/course/',
            {"name": "ABC", "description": "description"}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_subscription_create(self):
        """тест на создание подписки(неактивная по дефолту)"""
        self.test_course_create()
        response = self.client.post(
            '/department/subscriber/',
            {"courses": 1}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
    def test_subscription_update(self):
        self.test_subscription_create()
        response = self.client.put(
            f'/department/subscriber/1/',
            {"courses": 1, "is_active": True}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_course(self):
        '''проверка отображения подписки в
        курсе в зависимости от ее активности'''
        self.test_subscription_create()
        response = self.client.get(
            f'/department/course/1/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "pk": 1,
                "name": "ABC",
                'description': "description",
                "owner": 1,
                "count_lesson": 0,
                "lessons": [],
                "subscription": "Подписка отсутствует"
            }
        )

        self.test_subscription_update()
        response = self.client.get(
            f'/department/course/1/'
        )

        self.assertEqual(
            response.json(),
            {
                "pk": 1,
                "name": "ABC",
                'description': "description",
                "owner": 1,
                "count_lesson": 0,
                "lessons": [],
                "subscription": "Подписка оформлена"
            }
        )


