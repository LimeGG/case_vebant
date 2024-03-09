from drf_spectacular.utils import extend_schema
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import User, Competence, Review
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serialaize import UsersusSerializer, ReviewSerialize, ReviewSerializeCreate, MarkedCompetenceSerializeUs
from main.serialaize import CompetenceSerializer


class UserAll(APIView):
    serializer_class = UsersusSerializer

    def get(self, request, format=None):
        users = User.objects.all()
        serialize = UsersusSerializer(users, many=True)
        return Response(serialize.data)


class DetailUser(APIView):
    serializer_class = UsersusSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get(self, request, format=None):
        user = request.user  # Получение текущего пользователя
        serializer = UsersusSerializer(user)  # Сериализация текущего пользователя
        return Response(serializer.data)


class CompetenceMaterialAll(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    required_headers = {
        'Authorization': 'Bearer <токен>',
        'Content-Type': 'application/json'
    }
    serializer_class = CompetenceSerializer

    def get_queryset(self):
        return Competence.objects.prefetch_related('material_set').filter(is_active=True)


class CompetenceDetailUs(APIView):
    permission_classes = [permissions.IsAuthenticated]
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


class ListReview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = ReviewSerialize

    def get(self, request, format=None):
        user = request.user
        review = Review.objects.filter(user=user)
        serializer = ReviewSerialize(review)
        return Response(serializer.data)


class AddReview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = ReviewSerializeCreate

    def post(self, request, name, format=None):
        serializer = ReviewSerializeCreate(data=request.data)
        competence = Competence.objects.get(name=name)
        if serializer.is_valid():
            serializer.save(user=request.user, competence=competence)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = ReviewSerialize

    def get_review(self, review_id):
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None

    def put(self, request, review_id, format=None):
        review = self.get_review(review_id)
        if not review:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        if review.user != request.user:
            return Response({"error": "You are not allowed to edit this review"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerialize(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id, format=None):
        review = self.get_review(review_id)
        if not review:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        if review.user != request.user:
            return Response({"error": "You are not allowed to delete this review"}, status=status.HTTP_403_FORBIDDEN)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddCompetence(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    serializer_class = MarkedCompetenceSerializeUs

    def post(self, name, request, format=None):
        serializer = MarkedCompetenceSerializeUs(data=request.data)
        competence = Competence.objects.get(name=name)
        if serializer.is_valid():
            serializer.save(user=request.user, competence=competence)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        try:
            competence = Competence.objects.get(name=name)
            marked_competence = MarkedCompetence.objects.get(user=request.user, competence=competence)
        except (Competence.DoesNotExist, MarkedCompetence.DoesNotExist):
            return Response({"error": "Competence not found for the current user"}, status=status.HTTP_404_NOT_FOUND)

        marked_competence.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
