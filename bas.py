import os

from flask_migrate import Migrate

from app import create_app
from app import db
from app.models import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)  # migration engine


# for the flask shell command
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Job': Job, 'Company': Company}


@app.cli.command()
def test():
    """ Run the unit tests """
    import unittest
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')

    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run()
