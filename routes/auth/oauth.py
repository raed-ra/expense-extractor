# routes/auth/oauth.py

from flask import Blueprint, redirect, url_for, request, session, current_app
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from models.user import User
from db import get_db 
from flask_login import login_user
from .login import auth_bp  # import auth_bp from login.py
import os
import json

# config oauth client id
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

def create_flow():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('auth.oauth2callback', _external=True)
    )
    return flow

@auth_bp.route("/google")
def login_with_google():
    flow = create_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@auth_bp.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = create_flow()
    flow.fetch_token(
        authorization_response=request.url,
        state=state
    )
    
    credentials = flow.credentials
    id_info = id_token.verify_oauth2_token(
        credentials.id_token, requests.Request(), credentials.client_id
    )
    
    # get db session
    db = get_db()
    
    # check if user exists
    user = db.query(User).filter_by(oauth_id=id_info['sub']).first()
    
    if not user:
        # create new user
        user = User(
            email=id_info['email'],
            username=id_info.get('name', id_info['email'].split('@')[0]),
            oauth_provider='google',
            oauth_id=id_info['sub'],
            avatar=id_info.get('picture'),
            password=''  # oauth user doesn't need password
        )
        db.add(user)
        db.commit()
    
    # login user
    login_user(user)
    return redirect(url_for('home.index'))
