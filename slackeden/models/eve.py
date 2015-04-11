from slackeden import db
from .slack import Team


class Alliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    ticker = db.Column(db.String(32))
    corps = db.relationship('Corporation', backref='alliance', lazy='dynamic')

    @property
    def team(self):
        return Team.query.filter_by(alliance_id=self.id).first()


class Corporation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    ticker = db.Column(db.String(32))
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id'))
    members = db.relationship('User', backref='corporation', lazy='dynamic')

    @property
    def team(self):
        return Team.query.filter_by(corp_id=self.id).first()