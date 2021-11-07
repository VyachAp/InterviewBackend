from rest_framework.serializers import ModelSerializer
from interview.models import Scope


class ScopeSerializer(ModelSerializer):
    class Meta:
        model = Scope
        fields = "__all__"
