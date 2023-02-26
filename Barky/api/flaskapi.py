# python imports
# third-party imports
# your own imports

from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Charles Barky App"

# run flask using  flask --app api.flaskapi run --debug