from flask import Flask, url_for, redirect
from dotenv import load_dotenv
from os import getenv
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)


oauth = OAuth(app)

oauth.register(
    name='facebook',
    client_id=getenv("CLIENT_ID"),
    client_secret=getenv("CLIENT_SECRET"),
    access_token_url='https://graph.facebook.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://www.facebook.com/dialog/oauth',
    authorize_params=None,
    api_base_url='https://graph.facebook.com/',
    client_kwargs={'scope': 'email'},
)

app.secret_key = "my_secret_key"


@app.route("/login")
def login():
    facebook = oauth.create_client("facebook")    
    redirect_url = url_for("authorize", _external=True)
    return facebook.authorize_redirect(redirect_url)


@app.route("/authorize")
def authorize():
    facebook = oauth.create_client("facebook")   
    token = facebook.authorize_access_token()
    resp = facebook.get('https://graph.facebook.com/me?fields=id,name,email,picture{url}') 
    profile = resp.json()
    print(profile)
    return redirect("/")


@app.route("/")
def hello():
    return getenv("CLIENT_ID")


if __name__ == '__main__':
    load_dotenv()
