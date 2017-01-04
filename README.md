# Chess.com Puzzlers

## Running locally
```sh
$ pip install -r requirements.txt
$ npm install bower
$ bower install
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

## Deploying to Heroku
```sh
$ git push heroku master
$ heroku run python manage.py migrate

# First time only
$ heroku run python manage.py createsuperuser
```