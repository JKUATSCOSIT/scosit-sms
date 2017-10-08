# -*- coding: utf-8 -*-
"""Main application script
"""
import os

from flask_migrate import Migrate
from flask_script import Manager

from app import create_app

app = create_app(os.environ.get("APP_CONFIG", "default"))

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

manager = Manager(app=app)
migrate = Migrate(app=app)


@manager.shell
def make_shell_context():
    return dict(app=app)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'temp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://{covdir}index.html'.format(covdir=covdir))
        COV.erase()


if __name__ == "__main__":
    manager.run()