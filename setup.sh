python3 -m pip install whitenoise
python3 manage.py makemigrations home departments accounts codeshine
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic
python3 manage.py runserver