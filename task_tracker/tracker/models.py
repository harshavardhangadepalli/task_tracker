import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# these are the models used. ( Each model corresponds to a table in the database)

# represents the users object. The users are - USER, TEAM_MEMBER, TEAM_LEADER
class User(AbstractUser):
    ROLES_CHOICES = (
        ("USER", "USER"),
        ("TEAM_LEADER", "TEAM_LEADER"),
        ("TEAM_MEMBER", "TEAM_MEMBER"),
    )
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default="TEAM_MEMBER")
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(blank=False, null=False, unique=True)

    def __str__(self) -> str:
        return self.username


# represnts the team. The team will have a name, associated team leader, and team members.
# the team name needs to be unique. The team leader is a foreign key relationship on the User model.
# the team members is a many to many relationship. This means that many users can be part of one team, and one user can be part of many teams
class Team(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=20, blank=False, null=False, unique=True)
    team_leader = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    team_members = models.ManyToManyField(User, related_name="teams")


# represents the task that the user can create. Each task has a name, team that it is assigned to, task_memebers that are assigned to the task, etc.
# the team is a foreign key relation on the team team model.
# the task members is a many to many relationship between users and tasks.
class Task(models.Model):
    STATUS_CHOICES = (
        ("ASSIGNED", "ASSIGNED"),
        ("IN_PROGRESS", "IN_PROGRESS"),
        ("UNDER_REVIEW", "UNDER_REVIEW"),
        ("DONE", "DONE"),
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=20, blank=False, null=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    task_members = models.ManyToManyField(User, related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ASSIGNED")
    started_at = models.DateTimeField(default=datetime.now)
    completed_at = models.DateTimeField(default=datetime.now)
