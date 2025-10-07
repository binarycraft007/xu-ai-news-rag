import click
from flask import Flask
from flask.cli import with_appcontext
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from .config import Config
from .models import db
from .routes.main import main_bp
from .auth.routes import auth_bp
from .services.aggregation import run_aggregation_for_all_users
from .services.notification import mail

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    click.echo('Initialized the database.')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    JWTManager(app)
    mail.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Add the command to the app
    app.cli.add_command(init_db_command)

    # Setup scheduler
    scheduler = BackgroundScheduler()
    # Run in app context
    scheduler.add_job(
        func=lambda: app.app_context().push() or run_aggregation_for_all_users(),
        trigger="interval",
        hours=6
    )
    scheduler.start()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
