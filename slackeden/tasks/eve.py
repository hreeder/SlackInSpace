import evelink

from evelink.cache import sqlite
from slackeden import app, celery, db
from slackeden.models import User, Corporation, Alliance


@celery.task()
def update_corp_info(corpid):
    with app.app_context():
        corp = Corporation.query.filter_by(id=corpid).first()
        if corp:
            api = evelink.api.API(cache=sqlite.SqliteCache("eve-xml-api.cache"))
            corp_api = evelink.corp.Corp(api=api)
            info = corp_api.corporation_sheet(corp_id=corp.id).result

            changes = False

            # Corp not in right alliance
            if corp.alliance_id != info['alliance']['id']:
                corp.alliance_id = info['alliance']['id']
                changes = True

            if corp.ticker != info['ticker']:
                corp.ticker = info['ticker']
                changes = True

            if changes:
                db.session.add(corp)
                db.session.commit()


@celery.task()
def update_character_info(charid):
    with app.app_context():
        user = User.query.filter_by(id=charid).first()
        if user:
            api = evelink.api.API(cache=sqlite.SqliteCache("eve-xml-api.cache"))
            eve = evelink.eve.EVE(api)
            info = eve.character_info_from_id(user.id).result

            corp = Corporation.query.filter_by(id=info['corp']['id']).first()
            if not corp:
                corp = Corporation(
                    id=info['corp']['id'],
                    name=info['corp']['name']
                )
                db.session.add(corp)
                db.session.commit()

            celery.send_task('slackeden.tasks.eve.update_corp_info', [corp.id, ])

            user.corp_id = corp.id

            db.session.add(user)
            db.session.commit()


@celery.task()
def update_alliances():
    with app.app_context():
        api = evelink.api.API(cache=sqlite.SqliteCache("eve-xml-api.cache"))
        eve = evelink.eve.EVE(api)
        alist = eve.alliances().result

        for alliance_id in alist:
            alliance = Alliance.query.filter_by(id=alliance_id).first()
            if not alliance:
                alliance = Alliance(
                    id=alliance_id,
                    name=alist[alliance_id]['name'],
                    ticker=alist[alliance_id]['ticker']
                )
                db.session.add(alliance)
                db.session.commit()

            if alliance.ticker != alist[alliance_id]['ticker']:
                alliance.ticker = alist['alliance_id']['ticker']
                db.session.add(alliance)
                db.session.commit()
