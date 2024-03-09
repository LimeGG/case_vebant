from django.urls import path

from .views import UserRegistrationView, UserList, UserDetail, MarkedCompetenceAll, CompetenceAll, \
    CompetenceDetail, CompetenceCreate, CompetenceMaterialView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('users/competence/', MarkedCompetenceAll.as_view()),
    path('competence/', CompetenceAll.as_view()),
    path('competence/<str:name>', CompetenceDetail.as_view()),
    path('competence/create/', CompetenceCreate.as_view()),
    path('competence/<str:competence_name>/add_material/', CompetenceMaterialView.as_view(),
         name='add-material-to-competence'),
    path('competence/<str:competence_name>/materials/<int:material_id>/', CompetenceMaterialView.as_view()),
]