import flask
app = flask.Flask(__name__)

items = [
    {"header": "This is first post",
     "first": "Here is half of text",
     "second": "And second part of text"},
    {"header": "This is second post",
     "first": "Here is half of text",
     "second": "And second part of text"}
]


@app.route("/")
@app.route("/home")
def home():
    return flask.render_template("home.djhtml", posts=items, title="Home")


@app.route("/about")
def about():
    return flask.render_template("about.djhtml", title="About")
