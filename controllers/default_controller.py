import flask
import hashlib
import requests
import os
from datetime import datetime
from models.models import db
from models.models import User
from models.models import Posts
from decorator import decorator
from sqlalchemy.sql import select
from sqlalchemy.orm import session

'''
I don't really understand how Connexion works with Flask, so I'm using their example
https://github.com/zalando/connexion/blob/master/examples/basicauth/app.py
'''

def check_auth(username: str, password: str):
    select_stmt = select([User]).where(User.username == username)
    q = db.session.query(User).\
        select_entity_from(select_stmt)
    users = q.all()
    '''This function is called to check if a username /
    password combination is valid.'''
    return len(users)==1 and users[0].password == hashlib.sha256(password.encode()).hexdigest()

def authenticate():
    '''Sends a 401 response that enables basic auth'''
    resp = flask.jsonify({"code": 401, "message": "You need to be authenticated"})
    resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    resp.status_code = 401
    return resp

@decorator
def requires_auth(f: callable, *args, **kwargs):
    auth = flask.request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    return f(*args, **kwargs)

def name_to_id(username):
    select_stmt = select([User]).where(User.username == username)
    q = db.session.query(User).\
        select_entity_from(select_stmt)
    users = q.all()
    if len(users)==1:
        return users[0].id
    raise ValueError

@requires_auth
def status_annotate_post(id, body) -> str:
    return 'do some magic!'

@requires_auth
def status_home_tsurailine_get() -> str:
    return 'do some magic!'

@requires_auth
def status_update_post(file) -> str:
    res = requests.post(url='https://api.projectoxford.ai/emotion/v1.0/recognize',
                    data=file.read(),
                    headers={'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': os.environ['EMOTIONAPI_KEY']})
    if res.status_code==200:
        data = res.json()
        if len(data)>0:
            score = float(0)
            for face in data:
                candidate_score = (face['scores']['fear']+face['scores']['neutral']+face['scores']['sadness'])/float(3)
                if candidate_score > score:
                    score = candidate_score
        
        post = Posts(name_to_id(flask.request.authorization.username),score,datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        return flask.jsonify({"status_id":post.id})
    resp = flask.jsonify({"code": 400, "message": "Bad request"})
    resp.status_code = 401
    return resp

@requires_auth
def status_user_user_id_get(userId) -> str:
    return 'do some magic!'
