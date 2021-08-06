from rest_framework import viewsets
from interview.serializers.serializers import ScopeSerializer, SubScopeSerializer, ProfessionSerializer, \
    QuestionScopeSerializer, SuggestedQuestionsSerializer, PostCreateSerializer, PostsRetrieveSerializer,\
    PostLikeSerializer
from interview.models import Scope, SubScope, Profession, SuggestedQuestions, Post, PostLikes
from news_aggregator.serializers import NewsSerializer
from news_aggregator.models import Headline
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics


class ScopeView(viewsets.ModelViewSet):
    serializer_class = ScopeSerializer

    def get_queryset(self):
        professions = self.request.query_params.get('has_professions', False)
        if professions:
            return Scope.objects.filter(has_professions=True)
        return Scope.objects.all()


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

    def retrieve(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)


class CreatePostView(viewsets.ModelViewSet):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()

    def partial_update(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, requset, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)


class RetrievePostsView(viewsets.ModelViewSet):
    serializer_class = PostsRetrieveSerializer
    queryset = Post.objects.filter(status='Published')

    def create(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response('Not implemented', status.HTTP_405_METHOD_NOT_ALLOWED)


class PostLikeView(viewsets.ModelViewSet):
    serializer_class = PostLikeSerializer
    queryset = PostLikes.objects.all()
    http_method_names = ('OPTIONS', 'POST', 'DELETE')
