from rest_framework import status
import random
from django.shortcuts import get_object_or_404
import bcrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Team, UserTeam
from .serializers import UserSerializer, TeamSerializer, UserTeamSerializer, UserSerializerForList , TeamSerializerForList ,UserTeamSerializer,UserTeamSerializerDetail,UserSerializerMail

class UserView(APIView):

    def patch(self, request, pk, format=None):
        # Récupère l'ID de l'utilisateur à partir des données JSON
        admin_id = request.data.get('admin_id')

        # Vérifie si l'utilisateur avec l'ID spécifié est un administrateur
        try:
            admin_user = User.objects.get(id_user=admin_id)
            if not admin_user.est_admin:
                return Response({"message": f"Accès refusé. Seuls les administrateurs peuvent utiliser cette fonction pour l'utilisateur avec l'ID {admin_id}."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"message": f"Utilisateur administrateur avec l'ID {admin_id} non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Récupère l'utilisateur à mettre à jour
        try:
            user = User.objects.get(id_user=pk)
        except User.DoesNotExist:
            return Response({"message": f"Utilisateur avec l'ID {pk} non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Continuer avec la logique de modification de l'utilisateur
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializerForList(users, many=True)
        return Response(serializer.data)
    

    def post(self, request, format=None):
        # Récupère le mot de passe à partir des données JSON
        raw_password = request.data.get('mot_de_passe')

        # Hache le mot de passe avec bcrypt
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())

        # Modifie le mot de passe dans les données de la requête
        request.data['mot_de_passe'] = hashed_password.decode('utf-8')

        # Récupère l'ID de l'utilisateur administrateur à partir des données JSON
        admin_id = request.data.get('admin_id')

        # Vérifie si l'utilisateur avec l'ID spécifié est un administrateur
        try:
            admin_user = User.objects.get(id_user=admin_id)
            if not admin_user.est_admin:
                return Response({"message": f"Accès refusé. Seuls les administrateurs peuvent utiliser cette fonction pour l'utilisateur avec l'ID {admin_id}."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"message": f"Utilisateur administrateur avec l'ID {admin_id} non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Continuer avec le reste de la logique de création d'utilisateur
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TeamView(APIView):

    def patch(self, request, pk, format=None):
        # Récupère l'ID de l'utilisateur à partir des données JSON
        admin_id = request.data.get('admin_id')

        # Vérifie si l'utilisateur avec l'ID spécifié est un administrateur
        try:
            user = User.objects.get(id_user=admin_id)
            if not user.est_admin:
                return Response({"message": f"Accès refusé. Seuls les administrateurs peuvent utiliser cette fonction pour l'utilisateur avec l'ID {admin_id}."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"message": f"Utilisateur avec l'ID {admin_id} non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Récupère l'équipe à mettre à jour
        try:
            team = Team.objects.get(id_team=pk)
        except Team.DoesNotExist:
            return Response({"message": f"Équipe avec l'ID {pk} non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        # Continuer avec la logique de modification de l'équipe
        serializer = TeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializerForList(teams, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Récupère l'ID de l'utilisateur à partir des données JSON
        admin_id = request.data.get('admin_id')

        # Vérifie si l'utilisateur avec l'ID spécifié est un administrateur
        try:
            user = User.objects.get(id_user=admin_id)
            if not user.est_admin:
                return Response({"message": f"Accès refusé. Seuls les administrateurs peuvent utiliser cette fonction pour l'utilisateur avec l'ID {admin_id}."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"message": f"Utilisateur avec l'ID {admin_id} non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Continuer avec la logique d'insertion de l'équipe
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class user_teamView(APIView):

    def get(self, request, format=None):
        # Récupère toutes les équipes
        teams = Team.objects.all()
        team_data = []

        for team in teams:
            # Récupère les utilisateurs associés à chaque équipe
            users = User.objects.filter(userteam__team=team)
            user_serializer = UserSerializerMail(users, many=True)
            team_data.append({team.nom_team: user_serializer.data})

        return Response(team_data)

    def post(self, request, format=None):
        serializer = UserTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class RandomizeTeamsView(APIView):
    def post(self, request, format=None):
        # Récupère toutes les équipes existantes
        teams = list(Team.objects.all())
        # Récupère tous les utilisateurs existants
        users = list(User.objects.all())

        # Vérifie qu'il y a au moins une équipe et un utilisateur
        if not teams or not users:
            return Response({"message": "Impossible de répartir les utilisateurs, car il n'y a pas assez d'équipes ou d'utilisateurs."}, status=status.HTTP_400_BAD_REQUEST)

        # Mélange aléatoirement la liste des utilisateurs
        random.shuffle(users)

        # Réinitialise les associations utilisateur-équipe existantes
        UserTeam.objects.all().delete()

        # Associe chaque utilisateur à une équipe
        for i, user in enumerate(users):
            team = teams[i % len(teams)]
            UserTeam.objects.create(user=user, team=team)

        return Response({"message": "Les utilisateurs ont été répartis de manière aléatoire parmi les équipes existantes."}, status=status.HTTP_200_OK)