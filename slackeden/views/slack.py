from flask import render_template, request
from flask.ext.login import login_required, current_user
from slackeden import app, db
from slackeden.models import Team, TeamMember
from slackeden.models.slack import STATUS_OWNER
from slacker import Slacker


@app.route("/teams/add", methods=['GET', 'POST'])
@login_required
def add_team():
    if request.method == "POST":
        # Add a new Slack Team
        token = request.form['slacktoken']
        email = request.form['slackemail']
        corpteam = False
        allianceteam = False

        # We should check and find out if there's already a team for the user's corp
        corpteam_exists = Team.query.filter_by(corp_id=current_user.corp_id).first()

        # Check to see if this is indicated as a corp team
        if request.form.getlist('corpteam') and not corpteam_exists:
            corpteam = current_user.corp_id

        # Now we need to do the same for alliance, only if the user is in an alliance
        if current_user.corporation.alliance_id:
            allianceteam_exists = Team.query.filter_by(alliance_id=current_user.corporation.alliance_id).first()
            if request.form.getlist('allianceteam') and not allianceteam_exists:
                allianceteam = current_user.corporation.alliance_id

        # TODO: Improve reporting back to the user if their corp/alliance team could not be added


        slack = Slacker(token)
        teaminfo = slack.team.info().body['team']

        id = teaminfo['id']
        name = teaminfo['name']
        subdomain = teaminfo['domain']

        existing = Team.query.filter_by(id=id).first()
        if existing:
            # TODO: Improve the display of this message
            print "This team is already managed by SlackEden, please contact [the owner] for administrative access"

        team = Team(
            id=id,
            name=name,
            subdomain=subdomain,
            owner_id=current_user.id,
            token=request.form['slacktoken']
        )

        if corpteam:
            team.corp_id = corpteam
        if allianceteam:
            team.alliance_id = allianceteam

        db.session.add(team)
        db.session.commit()

        membership = TeamMember(
            team_id=id,
            user_id=current_user.id,
            email_address=email,
            status=STATUS_OWNER
        )

        db.session.add(membership)
        db.session.commit()

    return render_template("add_team.html")

@app.route("/teams/<id>/join", methods=["GET", "POST"])
@login_required
def join_team(id):
    team = Team.query.filter_by(id=id).first_or_404()

    # TODO: Check Access
    if team.corp_id and team.corp_id != current_user.corp_id:
        pass

    if team.alliance_id and team.alliance_id != current_user.corporation.alliance_id:
        pass

    return render_template("team_invite.html", team=team)