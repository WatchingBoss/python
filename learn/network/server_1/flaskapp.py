from flask import Flask
from flask import Response
flask_app = Flask("flaskapp")

@flask_app.route("/go")
def response():
    return Response("It works with Flask quite good\n",
                    mimetype = "text/plain")

app = flask_app.wsgi_app
