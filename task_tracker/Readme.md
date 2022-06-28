## Task Tracker

### To run 
* Start Redis on wsl ubuntu py running `redis-cli`
* Start Celery in another window inside the virtual environment by running `celery -A task_tracker worker -l info`
* Start task_trakcer server by running `python manage.py runserver` in virtual environment

### Some description for the URLs:
* "users" : to create a user.
* "users/<uuid:user_uid>" : to get a specific user with the corresponding userid.
* "all-users" : to get all users.
* "login" : to login.
* "create-team" : to create a team.
* "teams" : to get all teams.
* "teams/<uuid:team_uid>" : to get a specific team with the corresponding id.
* "create-task" : to create a task.
* "update-task" : to  update a task.
* "all-tasks" : to get all the tasks.


#### login:
* The login view allows a specific user to login using their username and password. 
* The password is stored using a hash.
* If login is successful, the response returns a token. This token can now be used for all subsequent queries, and authentication is taken care of using the token.


#### create-team:
* This will create a team based on the input parameters from the post request. 
* The fields are: id (needs to be a uuid generated), name(needs to be unique), team_leader (UUID of User), team_members (list of uuids)
* Only the users with the role "user" can create a team, and assign team leader.

### create-task:
* Task is created. The fields in the POST request are: id (uuid that is generated), name(name of the task), team(team to which the task is assigned), task_members(the team members of the team that the task is assigned to), status, started_at, and completed_at.
* Only users with the role USER will be able to create tasks

### update-task:
* An existing task can be updated. 
* Users of the rols TEAM_LEADER can change all fields of the task. But users of the role TEAM_MEMBER can only change the status field.

### get all tasks:
* Anyone can get a list of all the tasks that have been created.
