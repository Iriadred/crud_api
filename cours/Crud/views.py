from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserTeam


class ClearUserTeamView(APIView):
    def post(self, request, format=None):
        # Supprime toutes les entrées dans la table UserTeam
        UserTeam.objects.all().delete()
        return Response({"message": "La table UserTeam a été vidée avec succès."}, status=status.HTTP_200_OK)

def hello_world(request):
    return HttpResponse('Hello World !')
# Create your views here.
