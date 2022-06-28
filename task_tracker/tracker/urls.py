from django.urls import path

from tracker import views

urlpatterns = [
    path("users", views.create_user),
    path("users/<uuid:user_uid>", views.get_user),
    path("all-users", views.get_all_users),
    path("login", views.login),
    path("create-team", views.create_team),
    path("teams", views.get_all_teams),
    path("teams/<uuid:team_uid>", views.get_team),
    path("create-task", views.create_task),
    path("update-task", views.update_task),
    path("all-tasks", views.get_all_tasks),
]
