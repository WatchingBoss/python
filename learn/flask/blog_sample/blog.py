import flask
app = flask.Flask(__name__)


@app.route("/about")
def about():
    return flask.render_template("about.html")


@app.route("/")
@app.route("/home")
def home():
    return flask.render_template("home.html")
