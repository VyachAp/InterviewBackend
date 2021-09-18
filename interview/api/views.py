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
        questions = self.request.query_params.get('has_questions', False)
        return Scope.objects.filter(has_professions=professions, has_questions=questions)


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

    def create(self, request, *args, **kwargs):
        html = self.request.data['body'].get('html', None)
        if not html:
            return Response('Bad request', status.HTTP_400_BAD_REQUEST)
        self.request.data['body'] = html
        self.request.data['author'] = self.request.user.id
        return super().create(request, *args, **kwargs)

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

    def create(self, request, *args, **kwargs):
        if PostLikes.objects.filter(post_id=request.data['post'], user=self.request.user).exists():
            PostLikes.objects.filter(post_id=request.data['post'], user=self.request.user).delete()
            return Response('Successfully unliked', status.HTTP_204_NO_CONTENT)
        PostLikes.objects.create(post_id=request.data['post'], user=self.request.user)
        return Response('Successfully liked', status.HTTP_200_OK)
