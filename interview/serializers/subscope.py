from rest_framework.serializers import ModelSerializer
from interview.models import SubScope


class SubScopeSerializer(ModelSerializer):
    class Meta:
        model = SubScope
        fields = '__all__'
