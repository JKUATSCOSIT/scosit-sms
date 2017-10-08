# -*- coding: utf-8 -*-
"""Main application script
"""
import os

from flask_migrate import Migrate

from app import create_app

app = create_app(os.environ.get("APP_CONFIG", "default"))

migrate = Migrate()


@app.shell_context_processor
def make_shell_context():
    return dict(app=app)


