# -*- coding: utf-8 -*-

import os

from app import create_app, celery

app = create_app(os.environ.get("APP_CONFIG", "default"))

app.app_context().push()
