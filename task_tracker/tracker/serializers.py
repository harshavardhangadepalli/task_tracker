from rest_framework import serializers

from tracker.models import Task, Team, User


# serializer used to serialize users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "role", "username", "email"]


# used to serialize users while creation of users
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "role", "username", "email", "password"]
        

# usedto serialize team objects
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "team_leader", "team_members"]

# used to serialize while creation of new team
class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "team_leader", "team_members"]

# used to serialize team ojects, both while creation and updation/fetching
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "team",
            "task_members",
            "status",
            "started_at",
            "completed_at",
        ]

# used to serialize when the TEAM_MEMBER is trying to update the status.
class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "status"]