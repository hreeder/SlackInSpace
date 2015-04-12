from slackeden import db


class Team(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    subdomain = db.Column(db.String(64))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token = db.Column(db.String(64))
    corp_id = db.Column(db.Integer, db.ForeignKey('corporation.id'), nullable=True)
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id'), nullable=True)