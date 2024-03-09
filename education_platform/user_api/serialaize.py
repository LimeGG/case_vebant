from rest_framework import serializers

from main.models import User, MarkedCompetence, Competence, Material, Review


class UsersusSerializer(serializers.ModelSerializer):
    competence = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'is_active', 'is_superuser', 'profession', 'username', 'competence']

    def get_competence(self, user):
        competence = MarkedCompetence.objects.filter(user=user)
        return MarkedCompetenceSerializeUs(competence, many=True).data


class MarkedCompetenceSerializeUs(serializers.ModelSerializer):
    class Meta:
        model = MarkedCompetence
        fields = ['competence']


class ReviewSerialize(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['competence', 'user', 'rating', 'comment']


class ReviewSerializeCreate(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


