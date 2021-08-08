# Notes to breathe life into this project

## Venv

1. install virtualenv
2. `virtualenv .venv`
3. `. .venv/bin/activate`
   - verify that venv is activated: `which python` should point to the binary in .venv
4. `pip install django`

## Migrate (whatever that is) 
1. change Battleships.battleships.apps.BattleshipsConfig.name to "Battleships"
2. `python manage.py makemigrations Battleships`   
3. `python manage.py migrate Battleships`
3. `python manage.py --run-syncdb`
   
## Create superuser
1. `python manage.py createsuperuser`
2. follow prompts

## Start server
1. `python manage.py runserver`
2. you will get a URL on where to reach admin pages
