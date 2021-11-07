from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField
from interview.models import Account, SuggestedQuestions


class UserSerializer(ModelSerializer):
    suggested_questions_count = SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            'id', 'username', 'name', 'surname', 'phone', 'avatar', 'date_of_birth', 'sex', 'country', 'city',
            'last_login',
            'date_joined', 'suggested_questions_count')
        read_only_fields = ('id', 'phone', 'last_login', 'is_active', 'date_joined')

    def get_suggested_questions_count(self, obj):
        return SuggestedQuestions.objects.filter(user=obj).count()


class AccountLoginSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone']


class AccountVerifySerializer(ModelSerializer):
    code = IntegerField()

    class Meta:
        model = Account
        fields = ['phone', 'code']


class UserShortSerializer(UserSerializer):
    class Meta:
        model = Account
        fields = ('username',)