from rest_framework.serializers import ModelSerializer, SerializerMethodField
from interview.models import Post, PostLikes, PostComments, Account


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body', 'author',)


class PostCommentsSerializer(ModelSerializer):
    class Meta:
        model = PostComments
        fields = '__all__'


class PostsRetrieveSerializer(ModelSerializer):
    likes = SerializerMethodField()
    comments = SerializerMethodField()
    author = SerializerMethodField()
    liked_by_current_user = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'status', 'additional_info', 'body', 'date_created', 'author', 'likes', 'comments',
                  'liked_by_current_user')

    def get_likes(self, obj):
        return PostLikes.objects.filter(post=obj).count()

    def get_comments(self, obj):
        return PostCommentsSerializer(PostComments.objects.filter(post=obj).order_by('date_created'), many=True).data

    def get_author(self, obj):
        return obj.author.username

    def get_liked_by_current_user(self, obj):
        if isinstance(self.context['request'].user, Account):
            return bool(PostLikes.objects.filter(post=obj, user_id=self.context['request'].user).exists())
        return False


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLikes
        fields = '__all__'
