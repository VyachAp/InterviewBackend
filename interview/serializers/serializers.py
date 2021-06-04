from rest_framework.serializers import ModelSerializer, IntegerField, SerializerMethodField
from interview.models import Scope, Questions, SubScope, Profession, Account, ProfessionSalaries, ProfessionLinks


class ScopeSerializer(ModelSerializer):
    class Meta:
        model = Scope
        fields = "__all__"


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Questions
        fields = ("question", "answer")


class QuestionScopeSerializer(ModelSerializer):
    questions = SerializerMethodField()

    class Meta:
        model = Scope
        fields = ('id', 'name', 'questions')

    def get_questions(self, obj):
        questions = []
        for sub_scope in SubScope.objects.filter(scope_id=obj.id):
            questions.append({sub_scope.name: QuestionSerializer(Questions.objects.filter(subscope_id=sub_scope.id), many=True).data})
        return questions


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


class ProfessionSalariesSerializer(ModelSerializer):
    class Meta:
        model = ProfessionSalaries
        fields = '__all__'


class ProfessionLinksSerializer(ModelSerializer):
    class Meta:
        model = ProfessionLinks
        fields = '__all__'
