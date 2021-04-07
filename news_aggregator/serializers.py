from rest_framework.serializers import ModelSerializer
from news_aggregator.models import Headline


class NewsSerializer(ModelSerializer):
    class Meta:
        model = Headline
        fields = "__all__"
