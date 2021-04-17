from rest_framework.serializers import ModelSerializer, IntegerField
from interview.models import Scope, Questions, SubScope, Profession, Account


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


class ProfessionSerializer(ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'phone', 'username', 'last_login', 'is_active', 'date_joined']
        read_only_fields = ('last_login', 'is_active', 'date_joined')


class AccountLoginSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone']


class AccountVerifySerializer(ModelSerializer):
    code = IntegerField()

    class Meta:
        model = Account
        fields = ['phone', 'code']
