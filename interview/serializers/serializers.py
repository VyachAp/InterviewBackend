from rest_framework.serializers import ModelSerializer, CharField
from interview.models import Scope, Questions, SubScope


class ScopeSerializer(ModelSerializer):
    class Meta:
        model = Scope
        fields = "__all__"


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'


class SubScopeSerializer(ModelSerializer):
    class Meta:
        model = SubScope
        fields = '__all__'
