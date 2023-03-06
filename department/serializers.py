from rest_framework import serializers

from department.models import Course, Lesson, UserSubscription, Payment
from department.validators import LessonAndCourseValidatr


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'pk',
            'name',
            'preview',
            'link',
            'course_id',

        )
        validators = [LessonAndCourseValidatr(field='link')]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'pk',
            'name',
            'description',
            'count_lesson',
            'lessons',
            'subscription',
        )
        validators = [LessonAndCourseValidatr(field='description')]

    def get_count_lesson(self, instance):
        count_lesson = Lesson.objects.filter(course=instance).count()
        return count_lesson

    def get_subscription(self, pk):
        subscription = UserSubscription.objects.filter(courses_id=pk).filter(is_active=True)
        if subscription:
            return f'Подписка оформлена'
        return 'Подписка отсутствует'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'