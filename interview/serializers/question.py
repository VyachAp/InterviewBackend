from rest_framework.serializers import ModelSerializer, SerializerMethodField
from interview.models import Questions, Scope, SubScope, SuggestedQuestions


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Questions
        fields = ("id", "question", "answer")


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


class SuggestedQuestionsSerializer(ModelSerializer):
    class Meta:
        model = SuggestedQuestions
        fields = '__all__'
