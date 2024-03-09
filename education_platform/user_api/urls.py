from django.urls import path

from .views import UserAll, DetailUser, CompetenceMaterialAll, CompetenceDetailUs, ListReview, AddReview, ReviewUpdate, \
    AddCompetence

urlpatterns = [
    path('', UserAll.as_view()),
    path('me/', DetailUser.as_view()),
    path('competence/', CompetenceMaterialAll.as_view()),
    path('competence/detail/<str:name>', CompetenceDetailUs.as_view()),
    path('competence/me/review/', ListReview.as_view()),
    path('competence/<str:name>/review/create', AddReview.as_view()),
    path('competence/me/review/<int:review_id>', ReviewUpdate.as_view()),
    path('competence/add/<str:name>', AddCompetence.as_view()),

]