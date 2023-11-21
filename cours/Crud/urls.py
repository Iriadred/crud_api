from django.urls import path
from . import views
from .rest_views import UserView , TeamView ,user_teamView ,RandomizeTeamsView
from .views import ClearUserTeamView 



## ici on met les routes
urlpatterns = [
    path('hello/', views.hello_world),
    path('users/', UserView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserView.as_view(), name='user-detail'),
    path('team/', TeamView.as_view(), name='team-list'),
    path('team/<int:pk>/', TeamView.as_view(), name='team-list'),
    path('user_team/', user_teamView.as_view(), name='user_team-list'),
    path('user_team/sup/', ClearUserTeamView.as_view(), name='clear-user-team'),
    path('user_team/random/', RandomizeTeamsView.as_view(), name='randomize-teams'),
]