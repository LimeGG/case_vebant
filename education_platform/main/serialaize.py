from rest_framework import serializers
from .models import User, MarkedCompetence, Competence, Material


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'profession', 'username']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UsersSerializer(serializers.ModelSerializer):
    competence = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'is_active', 'is_staff', 'is_superuser', 'email', 'profession', 'username', 'competence']

    def get_competence(self, user):
        materials = MarkedCompetence.objects.filter(user=user)
        return MaterialSerializer(materials, many=True).data





class MarkedCompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkedCompetence
        fields = ['user', 'competence']


class MaterialSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)

    class Meta:
        model = Material
        fields = ('id', 'material_type', 'title', 'link', 'content', 'file')


class CompetenceSerializer(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Competence
        fields = ('id', 'name', 'description', 'difficulty', 'is_active', 'materials',)

    def get_materials(self, competence):
        materials = Material.objects.filter(competence=competence)
        return MaterialSerializer(materials, many=True).data
