from rest_framework.serializers import ModelSerializer, SerializerMethodField
from interview.models import Profession, ProfessionSalaries, ProfessionLinks


class ProfessionSalariesSerializer(ModelSerializer):
    class Meta:
        model = ProfessionSalaries
        fields = '__all__'


class ProfessionLinksSerializer(ModelSerializer):
    class Meta:
        model = ProfessionLinks
        fields = '__all__'


class ProfessionSerializer(ModelSerializer):
    salaries = SerializerMethodField()
    links = SerializerMethodField()

    class Meta:
        model = Profession
        fields = '__all__'

    def get_salaries(self, obj):
        return ProfessionSalariesSerializer(ProfessionSalaries.objects.filter(profession=obj.id), many=True).data

    def get_links(self, obj):
        return ProfessionLinksSerializer(ProfessionLinks.objects.filter(profession=obj.id), many=True).data
