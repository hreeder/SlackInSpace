import pycrest

from flask import render_template, redirect, url_for, request
from flask.ext.login import login_user, login_required, logout_user

from slackeden import app, db
from slackeden.models.user import User
from slackeden.tasks.eve import update_character_info

@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

@app.route("/")
@login_required
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    callback = url_for('logincallback', _external=True)
    eve = pycrest.EVE(client_id=app.config['EVESSO_CLIENT_ID'],
                      api_key=app.config['EVESSO_SECRET_KEY'],
                      redirect_uri=callback)
    return redirect(eve.auth_uri())

@app.route("/login/callback")
def logincallback():
    callback = url_for('logincallback', _external=True)
    code = request.args.get('code')

    eve = pycrest.EVE(client_id=app.config['EVESSO_CLIENT_ID'],
                      api_key=app.config['EVESSO_SECRET_KEY'],
                      redirect_uri=callback)
    con = eve.authorize(code)
    con()
    character = con.whoami()

    user = User.query.filter_by(id=character['CharacterID']).first()
    if not user:
        user = User(
            id=character['CharacterID'],
            name=character['CharacterName']
        )

        db.session.add(user)
        db.session.commit()

    login_user(user)

    update_character_info.delay(user.id)

    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))