from django.db import models

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, null=False)
    mail = models.EmailField(null=False, unique=True)
    mot_de_passe = models.CharField(max_length=256, null=False)
    est_admin = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.nom

class Team(models.Model):
    id_team = models.AutoField(primary_key=True)
    nom_team = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nom_team

class UserTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'team')  # Assurez-vous de ne pas avoir de doublons

    def __str__(self):
        return f"{self.user.nom} - {self.team.nom_team}"
