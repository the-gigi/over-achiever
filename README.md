# over-achiever
A little demo app that show how to create a REST API with Flask. 
It supports this DevX article: [Authenticate RESTful APIs with an OAuth provider](http://www.devx.com/webdev/authenticate-restful-apis-with-an-oauth-provider.html)

Uses Flask-RESTful, SQLAlchemy and Flask-SQLAlchemy.

The only somewhat fancy stuff is a self-referential Goal model, which allows
creating arbitrarily deep hierarchies of goals and sub-goals.

# Authentication
The over-achiever web app utilizes OAuth2 authentication via Github. You must
have a github account and hit the /login endpoint. This will direct you to
a Github login dialog, which will result in a page with a JSON 
response that includes a field called access-token. When you hit the API
you must provide the access token as a header


    curl -H "Access-Token:<the access token" http://localhost:5000/v1.0/goals
