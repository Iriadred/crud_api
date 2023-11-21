from rest_framework import serializers
from .models import User, Team, UserTeam

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'nom', 'mail', 'mot_de_passe', 'est_admin']


class UserSerializerMail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mail','nom']

class UserSerializerForList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nom','mail']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class TeamSerializerForList(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['nom_team']

class UserTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTeam
        fields = '__all__'



class UserTeamSerializerDetail(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    team = TeamSerializer()

    class Meta:
        model = UserTeam
        fields = ['user', 'team']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['team'] = representation['team']['nom_team']
        return representation