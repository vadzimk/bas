import os

from bas_app import create_app, ext_celery, db
from bas_app.models import Job, Company

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
celery = ext_celery.celery

print('hello from app.py')


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
