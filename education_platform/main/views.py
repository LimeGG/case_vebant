from django.http import Http404

from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, permissions

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serialaize import UserSerializer, UsersSerializer, MarkedCompetenceSerializer, \
    CompetenceSerializer, MaterialSerializer, ProfessionSerialize
from .models import User, MarkedCompetence, Competence, Material, Profession


@extend_schema(
    description="регистрация пользователя",
    summary="регистрация"
)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


##### Для Администратора
class MarkedCompetenceAll(APIView):
    serializer_class = MarkedCompetenceSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (JWTAuthentication,)

    @extend_schema(
        description="Получение компетенций пользователя",
        summary="Компетенции пользователя"
    )
    def get(self, request, format=None):
        competence = MarkedCompetence.objects.all()
        serializer = MarkedCompetenceSerializer(competence, many=True)
        return Response(serializer.data)


class UserList(APIView):
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (JWTAuthentication,)
    requires_authentication = True
    required_headers = {
        'Authorization': 'Bearer <токен>',
        'Content-Type': 'application/json'
    }

    @extend_schema(
        description="Получение списка всех пользователей",
        summary="Все пользователи"
    )
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    serializer_class = UsersSerializer

    # permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404

    @extend_schema(
        description="Получение одного пользователя",
        summary="пользователь"
    )
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        description="Изменение одного пользователя",
        summary="пользователь"
    )
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="получение всех компетенций",
    summary="Компетенции"
)
class CompetenceAll(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (JWTAuthentication,)
    requires_authentication = True
    required_headers = {
        'Authorization': 'Bearer <токен>',
        'Content-Type': 'application/json'
    }
    serializer_class = CompetenceSerializer

    def get_queryset(self):
        return Competence.objects.prefetch_related('material_set').all()


class CompetenceDetail(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (JWTAuthentication,)
    requires_authentication = True
    required_headers = {
        'Authorization': 'Bearer <токен>',
        'Content-Type': 'application/json'
    }
    serializer_class = CompetenceSerializer

    # permission_classes = [permissions.IsAdminUser]

    def get_object(self, name):
        try:
            return Competence.objects.get(name=name)
        except Competence.DoesNotExist:
            raise Http404

    @extend_schema(
        description="Получение одной компетенции",
        summary="компетенция"
    )
    def get(self, request, name, format=None):
        competence = self.get_object(name)
        serializer = CompetenceSerializer(competence)
        return Response(serializer.data)

    @extend_schema(
        description="Изменение одной компетенции",
        summary="компетенция"
    )
    def put(self, request, name, format=None):
        competence = self.get_object(name)
        serializer = CompetenceSerializer(competence, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompetenceCreate(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (JWTAuthentication,)
    requires_authentication = True
    required_headers = {
        'Authorization': 'Bearer <токен>',
        'Content-Type': 'application/json'
    }
    serializer_class = CompetenceSerializer

    @extend_schema(
        description="Создание новой компетенции",
        summary="компетенция"
    )
    def post(self, request, format=None):
        serializer = CompetenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompetenceMaterialView(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (JWTAuthentication,)
    requires_authentication = True
    required_headers = {
        'Authorization': 'Bearer <токен>',
        'Content-Type': 'application/json'
    }
    serializer_class = MaterialSerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        description="Создание материала для компетенции",
        summary="Материал"
    )
    def post(self, request, competence_name, format=None):
        try:
            competence = Competence.objects.get(name=competence_name)
        except Competence.DoesNotExist:
            return Response({"error": "Competence not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(competence=competence)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (JWTAuthentication,)
    requires_authentication = True
    required_headers = {
        'Authorization': 'Bearer <токен>',
        'Content-Type': 'application/json'
    }
    serializer_class = MaterialSerializer

    @extend_schema(
        description="Получение, обновление или удаление материала компетенции",
        summary="Материал"
    )
    def get(self, request, competence_name, material_id, format=None):
        try:
            competence = Competence.objects.get(name=competence_name)
            material = Material.objects.get(id=material_id, competence=competence)
        except (Competence.DoesNotExist, Material.DoesNotExist):
            return Response({"error": "Competence or material not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MaterialSerializer(material)
        return Response(serializer.data)

    @extend_schema(
        description="Обновление материала компетенции",
        summary="Материал"
    )
    def put(self, request, competence_name, material_id, format=None):
        try:
            competence = Competence.objects.get(name=competence_name)
            material = Material.objects.get(id=material_id, competence=competence)
        except (Competence.DoesNotExist, Material.DoesNotExist):
            return Response({"error": "Competence or material not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Удаление материала компетенции",
        summary="Материал"
    )
    def delete(self, request, competence_name, material_id, format=None):
        try:
            competence = Competence.objects.get(name=competence_name)
            material = Material.objects.get(id=material_id, competence=competence)
        except (Competence.DoesNotExist, Material.DoesNotExist):
            return Response({"error": "Competence or material not found"}, status=status.HTTP_404_NOT_FOUND)

        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

##### Для Администратора ^^^^^^^

########### Методы для создания професий удаление проф редактирование проф. Метод для добавления професии.Метод для просмотра юзера
class Profession(APIView):
    permission_classes = [AllowAny]
    authentication_classes = (JWTAuthentication,)
    required_headers = {
        'Authorization': 'Bearer <токен>',
        'Content-Type': 'application/json'
    }
    serializer_class = ProfessionSerialize

    @extend_schema(
        description="Создание Профессии",
        summary="Профессия"
    )
    def post(self, request, name, format=None):
        serializer = ProfessionSerialize(data=request.data)
        if serializer.is_valid():
            serializer.save(name=name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfEditing(APIView):
    permission_classes = [AllowAny]
    authentication_classes = (JWTAuthentication,)
    required_headers = {
        'Authorization': 'Bearer <токен>',
        'Content-Type': 'application/json'
    }
    serializer_class = ProfessionSerialize

    @extend_schema(
        description="Получение профессии",
        summary="Профессия"
    )
    def get(self, request, name, format=None):
        try:
            profession = Profession.objects.get(name=name)
        except (Profession.DoesNotExist,):
            return Response({"error": "Profession not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfessionSerialize(profession)
        return Response(serializer.data)

    @extend_schema(
        description="Обновление профессии",
        summary="Профессия"
    )
    def put(self, request, name, format=None):
        try:
            profession = Profession.objects.get(name=name)
        except (Profession.DoesNotExist,):
            return Response({"error": "Profession not fount"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfessionSerialize(profession, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Удаление Профессии",
        summary="Профессия"
    )
    def delete(self, request, name, format=None):
        try:
            profession = Profession.objects.get(name=name)
        except (Profession.DoesNotExist,):
            return Response({"error": "Profession not fount"}, status=status.HTTP_404_NOT_FOUND)

        profession.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)