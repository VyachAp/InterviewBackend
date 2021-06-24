from rest_framework.serializers import ModelSerializer, IntegerField, SerializerMethodField
from interview.models import Scope, Questions, SubScope, Profession, Account, ProfessionSalaries, ProfessionLinks, SuggestedQuestions


class ScopeSerializer(ModelSerializer):
    class Meta:
        model = Scope
        fields = "__all__"


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Questions
        fields = ("id","question", "answer")


class QuestionScopeSerializer(ModelSerializer):
    questions = SerializerMethodField()

    class Meta:
        model = Scope
        fields = ('id', 'name', 'questions')

    def get_questions(self, obj):
        questions = []
        for sub_scope in SubScope.objects.filter(scope_id=obj.id):
            questions.append({"subscope": sub_scope.name,
                              "subscope_id": sub_scope.id,
                              "questions": QuestionSerializer(Questions.objects.filter(subscope_id=sub_scope.id),
                                                              many=True).data})
        return questions


class SubScopeSerializer(ModelSerializer):
    class Meta:
        model = SubScope
        fields = '__all__'


class ProfessionSerializer(ModelSerializer):
    salaries = SerializerMethodField()

    class Meta:
        model = Profession
        fields = '__all__'

    def get_salaries(self, obj):
        return ProfessionSalariesSerializer(ProfessionSalaries.objects.filter(profession=obj.id), many=True).data


class UserSerializer(ModelSerializer):
    suggested_questions_count = SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'username', 'name', 'surname', 'phone', 'avatar', 'date_of_birth', 'sex', 'country', 'city', 'last_login', 'date_joined', 'suggested_questions_count')
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


class ProfessionSalariesSerializer(ModelSerializer):
    class Meta:
        model = ProfessionSalaries
        fields = '__all__'


class ProfessionLinksSerializer(ModelSerializer):
    class Meta:
        model = ProfessionLinks
        fields = '__all__'


class SuggestedQuestionsSerializer(ModelSerializer):
    class Meta:
        model = SuggestedQuestions
        fields = '__all__'
