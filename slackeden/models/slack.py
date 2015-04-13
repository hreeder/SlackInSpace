from slackeden import db

STATUS_MEMBER = 0
STATUS_ADMINISTRATOR = 1
STATUS_OWNER = 2


class Team(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    subdomain = db.Column(db.String(64))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token = db.Column(db.String(64))
    corp_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id'))


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String(64), db.ForeignKey('team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email_address = db.Column(db.String(128))
    slack_user_id = db.Column(db.String(64))
    status = db.Column(db.Integer, default=STATUS_MEMBER)
