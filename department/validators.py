from rest_framework import serializers

LINKS = "youtube"


class LessonAndCourseValidatr:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = value.get('link')
        description = value.get('description')
        error = serializers.ValidationError('Недопустимо загружать видео с любых площадок кроме You tube')

        if link:
            if LINKS not in link.split('.'):
                raise error

        elif 'https:' in description.split('/') and LINKS not in description.split('.'):
            raise error
