from flask.ext.login import UserMixin

from slackeden import db, lm


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    corp_id = db.Column(db.Integer, db.ForeignKey('corporation.id'))

    def get_corp_name(self):
        if self.corp_id and self.corporation.name:
            return self.corporation.name

    def get_corp_ticker(self):
        if self.corp_id and self.corporation.ticker:
            return "[" + self.corporation.ticker + "]"
        else:
            return ""

    def get_alliance_name(self):
        if self.corp_id and self.corporation.alliance_id and self.corporation.alliance.name:
            return self.corporation.alliance.name

    def get_alliance_ticker(self):
        if self.corp_id and self.corporation.alliance_id and self.corporation.alliance.ticker:
            return "<" + self.corporation.alliance.ticker + ">"
        else:
            return ""


@lm.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()