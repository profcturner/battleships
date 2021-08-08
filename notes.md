# Notes to breathe life into this project

## Venv

1. install virtualenv
2. `virtualenv .venv`
3. `. .venv/bin/activate`
   - verify that venv is activated: `which python` should point to the binary in .venv
4. `pip install django`

## Create super user   
1. change Battleships.battleships.apps.BattleshipsConfig.name to "Battleships"
2. `python manage.py migrate`
3. `python manage.py createsuperuser`
4. follow prompts
