@echo off
echo Running Django Migrations...
echo.
cd /d "%~dp0"
python manage.py makemigrations
python manage.py migrate
echo.
echo Migrations completed!
pause

