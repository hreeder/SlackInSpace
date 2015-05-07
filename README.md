# SlackInSpace

A tool to manage Slack Teams for EVE Online Corporations and Alliances (and more!)

## Installing
Create a config.py file. Ask Sklullus (@hreeder) for a dev copy while there isn't an anonymised version in the repo. You will need to register an application over on the [EVE Developers Site](https://developers.eveonline.com/) to fill out `EVESSO_CLIENT_ID` and `EVESSO_SECRET_KEY` in the config.

Install bower packages with `bower install`.

Apply database migrations with `python manage.py db upgrade` (This only applies generated migrations to your configured database)

Run development server with `python run_debug.py`

Server now running on [http://localhost:5000/](http://localhost:5000/)
