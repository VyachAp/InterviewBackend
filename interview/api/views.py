from rest_framework import viewsets
from interview.serializers import ScopeSerializer, SubScopeSerializer, ProfessionSerializer, \
    QuestionScopeSerializer, SuggestedQuestionsSerializer, PostCreateSerializer, PostsRetrieveSerializer,\
    PostLikeSerializer, FeedbackSerializer, CourseSerializer, QuestionSerializer
from interview.models import Scope, SubScope, Profession, SuggestedQuestions, Post, PostLikes, Feedback, Course, Questions
from news_aggregator.serializers import NewsSerializer
from news_aggregator.models import Headline
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics
import pandas as pd
import os
import sys


class ScopeView(viewsets.ModelViewSet):
    serializer_class = ScopeSerializer

    def get_queryset(self):
        professions = self.request.query_params.get('has_professions', False)
        questions = self.request.query_params.get('has_questions', False)
        if professions:
            return Scope.objects.filter(has_professions=professions)
        if questions:
            return Scope.objects.filter(has_questions=questions)

        return Scope.objects.all()


class NewsView(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = Headline.objects.order_by('-id')


class SubScopeView(viewsets.ModelViewSet):
    serializer_class = SubScopeSerializer

    def get_queryset(self):
        return SubScope.objects.filter(scope=self.request.query_params["scope"])


class QuestionsView(viewsets.ModelViewSet):
    # Ver.0.1.5
    serializer_class = QuestionScopeSerializer

    def get_queryset(self):
        return Scope.objects.filter(id=self.request.query_params['scope'])


class NewQuestionsView(viewsets.ModelViewSet):
    # Ver 0.1.6
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Questions.objects.filter(subscope_id=self.request.query_params['subscope'])


class ProfessionsView(viewsets.ModelViewSet):
    serializer_class = ProfessionSerializer

    def get_queryset(self):
        if self.request.query_params.get('scope', None):
            return Profession.objects.filter(scope=self.request.query_params['scope'])
        else:
            return Profession.objects.all()


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


class RetrievePostsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostsRetrieveSerializer
    queryset = Post.objects.filter(status='Published')


class PostLikeView(viewsets.ModelViewSet):
    serializer_class = PostLikeSerializer
    queryset = PostLikes.objects.all()

    def create(self, request, *args, **kwargs):
        if PostLikes.objects.filter(post_id=request.data['post'], user=self.request.user).exists():
            PostLikes.objects.filter(post_id=request.data['post'], user=self.request.user).delete()
            return Response('Successfully unliked', status.HTTP_204_NO_CONTENT)
        PostLikes.objects.create(post_id=request.data['post'], user=self.request.user)
        return Response('Successfully liked', status.HTTP_200_OK)


class FeedbackView(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()


class CourseView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(profession=self.request.query_params["profession"])


class UploadData(APIView):

    def post(self, request, *args, **kwargs):
        wses = {
            'Вопросы': Questions,
            'Профессии': Profession
        }
        work_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        file_path = f'{work_dir}/fixtures/update_questions.xlsx'
        worksheet = pd.ExcelFile(file_path)
        for sheet in worksheet.sheet_names:
            cur_model = wses[sheet]
            df = pd.read_excel(worksheet, sheet, header=0)
            for index, row in df.iterrows():
                if cur_model == Questions:
                    check_question = Questions.objects.filter(question=row[3]).exists()
                    if not check_question:
                        check_sphere = Scope.objects.filter(name=row[1]).exists()
                        if not check_sphere:
                            scope = Scope(name=row[1])
                            scope.save()
                            sub_scope = SubScope(name=row[2], scope_id=scope.id)
                            sub_scope.save()
                        else:
                            check_sub_scope = SubScope.objects.filter(name=row[2], scope=Scope.objects.filter(name=row[1]).first()).exists()
                            if not check_sub_scope:
                                sub_scope = SubScope(name=row[2], scope=Scope.objects.filter(name=row[1]).first())
                                sub_scope.save()
                            else:
                                sub_scope = SubScope.objects.filter(name=row[2], scope=Scope.objects.filter(name=row[1]).first()).first()

                        question = Questions(question=row[3], answer=row[4], subscope_id=sub_scope.id)
                        question.save()
                else:
                    check_profession = Profession.objects.filter(name=row[2]).exists()
                    if not check_profession:
                        check_sphere = Scope.objects.filter(name=row[1]).exists()
                        if not check_sphere:
                            scope = Scope(name=row[1])
                            scope.save()
                        else:
                            scope = Scope.objects.filter(name=row[1]).first()
                        profession = Profession(name=row[2], english_name=row[3], description=row[4], scope_id=scope.id)
                        profession.save()

        return Response({'data': worksheet.sheet_names}, status=200)
