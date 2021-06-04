from rest_framework import viewsets
from interview.serializers.serializers import ScopeSerializer, SubScopeSerializer, ProfessionSerializer, QuestionScopeSerializer
from interview.models import Scope, SubScope, Questions, Profession
from news_aggregator.serializers import NewsSerializer
from news_aggregator.models import Headline


class ScopeView(viewsets.ModelViewSet):
    serializer_class = ScopeSerializer
    queryset = Scope.objects.all()


class NewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = Headline.objects.order_by('-id')


class SubScopeView(viewsets.ModelViewSet):
    serializer_class = SubScopeSerializer

    def get_queryset(self):
        return SubScope.objects.filter(scope=self.request.query_params["scope"])


class QuestionsView(viewsets.ModelViewSet):
    serializer_class = QuestionScopeSerializer

    def get_queryset(self):
        return Scope.objects.filter(id=self.request.query_params['scope'])


class ProfessionsView(viewsets.ModelViewSet):
    serializer_class = ProfessionSerializer

    def get_queryset(self):
        return Profession.objects.filter(scope=self.request.query_params['scope'])

