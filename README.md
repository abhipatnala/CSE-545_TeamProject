# CSE-545_TeamProject

Python version : 3.8.9

Use Conda or venv to create virtual env for the team project
Use pyenv for handling multiple python versions

Above 2 packages need some configs in .bash or .zsh. so Read docs carefully. 

Clone the repository

1. Cd to project 
2. python3 -m venv ./venv --prompt she (command to create virtual env)
3. source venv/bin/activate (command to activate virtual env)
4. which python (command to check your python version, make sure it is 3.8.9)
5. pip install -r requirements.txt
6. python manage.py migrate (command to run migrations)
7. python manage.py runserver (command to run dev server)
8. Navigate to localhost:8000 in your browser to see app


In prod env, we are saving secrets in .env file, which is not compatiable in dev env. So in your local env, 

cd secure_hospital_system/settings.py

add this line to that file:

SECRET_KEY="1SVnU2FwIRetsvdkDn+y/2UpyhfsumGgPuQP6rlJo9Y="

Please do remember to delete this change, when you are raising pull request for merging to master.
