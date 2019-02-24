# Over-achiever
A little demo app that show how to create a REST API with Flask. 
It supports these DevX articles:

- [Writing RESTful Web Services in Python with Flask](http://www.devx.com/webdev/writing-restful-web-services-in-python-with-flask.html)
- [Authenticate RESTful APIs with an OAuth provider](http://www.devx.com/webdev/authenticate-restful-apis-with-an-oauth-provider.html)

Uses Flask-RESTful, SQLAlchemy and Flask-SQLAlchemy.

The only somewhat fancy stuff is a self-referential Goal model, which allows
creating arbitrarily deep hierarchies of goals and sub-goals.

# Running over-achiever locally

Make sure you got Docker and docker-compose installed.

Then just type: `docker-compose up`

# Authentication
The over-achiever web app utilizes OAuth2 authentication via Github. You must
have a github account and hit the `/login` endpoint. This will direct you to
a Github login dialog, which will result in a page with a JSON 
response that includes a field called access-token. When you hit the API
you must provide the access token as a header


## Getting all the goals for current user

I suggest ot store the token is an environment variable:

```
export OVER_ACHIEVER_TOKEN=<the acces token>
```


With HTTPie:
```
http http://localhost:5000/v1.0/goals "Access-Token:$OVER_ACHIEVER_TOKEN"
```

With cURL:
```
curl -H "Access-Token:$OVER_ACHIEVER_TOKEN" http://localhost:5000/v1.0/goals
```

## Adding a goal
With HTTPie:
```
http POST http://localhost:5000/v1.0/goals "Access-Token:OVER_ACHIEVER_TOKEN" name=<goal name>
```

