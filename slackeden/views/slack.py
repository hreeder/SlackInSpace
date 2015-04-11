from flask import render_template, request
from flask.ext.login import login_required
from slackeden import app


@app.route("/teams/add", methods=['GET', 'POST'])
@login_required
def add_team():
    if request.method == "POST":
        pass

    return render_template("add_team.html")