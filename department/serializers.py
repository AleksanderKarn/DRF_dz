from rest_framework import serializers

from department.models import Course, Lesson





class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'name',
            'link',
        )


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField() ## забыл скобочки просидел час....... спс pcharm за автозаполнение
    lessons = LessonSerializer(source='lesson_set', many=True)
    class Meta:
        model = Course
        fields = (
            'pk',
            'name',
            'description',
            'count_lesson',
            'lessons',

        )

    def get_count_lesson(self, instance):
        count_lesson = Lesson.objects.filter(course=instance).count()
        return count_lesson