from datetime import datetime
from uuid import UUID

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from tracker.models import Task, Team, User
from tracker.serializers import (
    CreateTeamSerializer,
    CreateUserSerializer,
    TaskSerializer,
    TeamSerializer,
    UserSerializer,
    UserTaskSerializer,
)

from .tasks import send_mail


# The view that is used to login as a user.
# this needs to be accessible to all the users, so the @permission_classes field is 'allow any'
# returns the token of authentication if successful. Otherwise returns 400 BAD Request
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request) -> Response:
    password = request.data["password"]
    username = request.data["username"]
    password = make_password(password)
    user = User.objects.get(username=username)
    if not user:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)


# the view that creates user.
@api_view(["POST"])
def create_user(request) -> Response:
    data = request.data
    serialized_data = CreateUserSerializer(data=data)
    if serialized_data.is_valid():
        user = serialized_data.save(
            password=make_password(serialized_data.validated_data["password"])
        )
        serialized_user = UserSerializer(data=user.__dict__)
        serialized_user.is_valid()
        return Response(serialized_user.data, status=status.HTTP_201_CREATED)
    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


# view that is used to get a specific user from the system.
@api_view(["GET"])
def get_user(request, user_uid: UUID) -> Response:
    user = User.objects.get(id=user_uid)
    serialized_user = UserSerializer(data=user.__dict__)
    if serialized_user.is_valid():
        return Response(serialized_user.data, status=status.HTTP_200_OK)
    return Response(serialized_user.data, status=status.HTTP_200_OK)


# the view that is used to get all the users that exist in the system.
@api_view(["GET"])
def get_all_users(request) -> Response:
    all_users = User.objects.all()
    serialized_users = UserSerializer(all_users, many=True)
    return Response(serialized_users.data, status=status.HTTP_200_OK)


# the view that is used to create a new team. Only the users with the role of 'USER' can create teams.
# returns 201 created if successful, otherwise returns 400 bad request
@api_view(["POST"])
def create_team(request) -> Response:
    data = request.data
    if request.user.role != "USER":
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    serialized_data = CreateTeamSerializer(data=data)
    if serialized_data.is_valid():
        serialized_data.save()
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)
    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


# View that is used to get all the teams in the system.
@api_view(["GET"])
def get_all_teams(request) -> Response:
    all_teams = Team.objects.all()
    serialized_teams = TeamSerializer(all_teams, many=True)
    return Response(serialized_teams.data, status=status.HTTP_200_OK)


# view that returns the team with a specific uuid
@api_view(["GET"])
def get_team(request, team_uid: UUID) -> Response:
    team = Team.objects.get(id=team_uid)
    serialized_team = TeamSerializer(data=team.__dict__)
    return Response(serialized_team.data, status=status.HTTP_200_OK)


# view that is used to create a new task. Only the users with the role of 'USER' is allowed to create a new task.
# returns 201 created if successful, otherwise returns 400 bad request
@api_view(["POST"])
def create_task(request) -> Response:
    data = request.data
    if request.user.role == "USER":
        serialized_data = TaskSerializer(data=data)
        if serialized_data.is_valid():
            task = serialized_data.save()
            team_leader = task.team.team_leader
            subject = f"Task {task.name} is created by {request.user.username} at {datetime.now()}"
            send_mail(request.user.email, [team_leader.email], subject)
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.data, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# this is the view that is used to update the task.
# the role of TEAM_LEADER can update all fields in the task (except id). But TEAM_MEMEBER can only update the status of the task.
# returns 200 OK if successful, otherwise returns 400 bad request
@api_view(["PATCH"])
def update_task(request) -> Response:
    data = request.data
    task = Task.objects.filter(id=data.get("id")).first()
    if request.user.role == "TEAM_LEADER":
        serialized_data = TaskSerializer(data=data)
        if serialized_data.is_valid() and task:
            task = serialized_data.update(task, serialized_data.validated_data)
            response_data = TaskSerializer(task)
            return Response(response_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.data, status=status.HTTP_400_BAD_REQUEST)
    elif request.user.role == "TEAM_MEMBER" and set(request.data.keys()) == {
        "id",
        "STATUS",
    }:
        serialized_data = UserTaskSerializer(data=data)
        if serialized_data.is_valid() and task:
            task = serialized_data.update(task, serialized_data.validated_data)
            response_data = TaskSerializer(task)
            return Response(response_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.data, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# this is the view that is used to get all the tasks in the system.
@api_view(["GET"])
def get_all_tasks(request) -> Response:
    all_tasks = Task.objects.all()
    serialized_tasks = TaskSerializer(all_tasks, many=True)

    return Response(serialized_tasks.data, status=status.HTTP_200_OK)
