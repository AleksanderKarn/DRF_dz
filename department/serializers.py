from rest_framework import serializers

from department.models import Course, Lesson





class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'name',
            'link',
            'owner',
        )


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    class Meta:
        model = Course
        fields = (
            'pk',
            'name',
            'description',
            'owner',
            'count_lesson',
            'lessons',

        )

    def get_count_lesson(self, instance):
        count_lesson = Lesson.objects.filter(course=instance).count()
        return count_lesson