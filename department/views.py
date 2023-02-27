from rest_framework import viewsets, generics

from rest_framework.permissions import IsAuthenticated

from department.models import Course, Lesson, UserSubscription
from department.permissions import OwnerOrStuff, IsOwner, IsStaff, PermsForViewSetCourse, IsNotStaff
from department.serializers import CourseSerializer, LessonSerializer, UserSubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    queryset = UserSubscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [PermsForViewSetCourse]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'moderator':
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    ##### CRUD для модели Lesson при помощи generics


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsStaff]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'moderator':
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsStaff]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsNotStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [OwnerOrStuff]


class LessonRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [OwnerOrStuff]
