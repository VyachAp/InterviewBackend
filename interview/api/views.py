from rest_framework import viewsets
from interview.serializers.serializers import ScopeSerializer, SubScopeSerializer, QuestionSerializer
from interview.models import Scope, SubScope, Questions
from news_aggregator.serializers import NewsSerializer
from news_aggregator.models import Headline


class ScopeView(viewsets.ModelViewSet):
    serializer_class = ScopeSerializer
    queryset = Scope.objects.all()


class NewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = Headline.objects.all()


class SubScopeView(viewsets.ModelViewSet):
    serializer_class = SubScopeSerializer

    def get_queryset(self):
        return SubScope.objects.filter(scope=self.request.query_params["scope"])


class QuestionsView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Questions.objects.filter(subscope=self.request.query_params['subscope'])