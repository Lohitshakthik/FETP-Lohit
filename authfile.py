import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request,render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from functools import wraps
from flask import session, redirect, url_for
from datetime import datetime
import pytz


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask("Google Login App")
app.secret_key = "Lohit@123"

google_client_id="120157765413-gbtht0gvbqddq1oia7qbe6a86hqrngo9.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")


flow=Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                   scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]
                                   ,redirect_uri="http://127.0.0.1:5000/callback")
def login_is_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper

def get_ist_time():
    return datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z%z')

@app.route("/login")
def login():

    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=google_client_id
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    return redirect("/protected_area")


@app.route("/Signout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():

    return f"Welcome <br> <a href='/login'><button>Login</button></a>"

def design_game():
    def print_diamond_pyramid(word, a):
        for i in range(1, a + 1, 2):
            spaces = " " * ((a - i) // 2)
            row = spaces + ''.join(word[:i]) + spaces
          print(row)
        for i in range(a - 2, 0, -2):
            spaces = " " * ((a - i) // 2)
            row = spaces + ''.join(word[:i]) + spaces
            print(row)
    word = "FormulaQSolutions"
    a = int(input("Enter the number of lines for the pyramid: "))

    print_diamond_pyramid(word, a)

@app.route("/play_game")
@login_is_required
def play_game():
    design_game()
    return "<br/><a href='/protected_area'><button>Back to Protected Area</button></a>"

@app.route("/protected_area")
@login_is_required
def protected_area():
    name = session.get('name')
    email = session.get('email')    
    return f"<br/> Hello {name}! <br/>You are signed in with the E-mail: {email} <br> <a href='/play_game'><button>Let's play game</button> </a> <br><a href='/Signout'><button>Signout</button></a></br>"

if __name__=="__main__":
    app.run(debug=True)


