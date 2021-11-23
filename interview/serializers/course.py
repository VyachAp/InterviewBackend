from rest_framework.serializers import ModelSerializer
from interview.models import Course


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'link', 'name')
