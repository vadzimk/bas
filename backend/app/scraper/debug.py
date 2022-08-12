import os
from app import create_app, db
from app.models import Job, Company

app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # access  flask-sqlalchemy
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
with app.app_context():
    result = db.session.query(Company, Job).join(Company).all()
    res = []
    for c, j in result:
        j_dict = j.__dict__
        j_dict.pop('_sa_instance_state', None)

        c_dict = c.__dict__
        c_dict.pop('_sa_instance_state', None)

        res.append({**j_dict, **c_dict})
print(res)