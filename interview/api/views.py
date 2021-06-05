from rest_framework import viewsets
from interview.serializers.serializers import ScopeSerializer, SubScopeSerializer, ProfessionSerializer, \
    QuestionScopeSerializer, SuggestedQuestionsSerializer
from interview.models import Scope, SubScope, Profession, SuggestedQuestions
from news_aggregator.serializers import NewsSerializer
from news_aggregator.models import Headline
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics

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


class SuggestedQuestionsView(viewsets.ModelViewSet):
    serializer_class = SuggestedQuestionsSerializer
    queryset = SuggestedQuestions.objects.all()

    def retrieve(self,  request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self,  request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)
