from datetime import datetime, time

from sqlalchemy import func, text
from sqlalchemy.ext.hybrid import hybrid_property

from . import db
from sqlalchemy.sql import expression
from sqlalchemy.dialects.postgresql import ARRAY


class Company(db.Model):
    __tablename__ = 'Company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rating = db.Column(db.String, nullable=True)
    industry = db.Column(db.String, nullable=True)
    size = db.Column(db.String, nullable=True)
    overview = db.Column(db.String, nullable=True)
    number_employees = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String, nullable=True)
    main_country_name = db.Column(db.String, nullable=True)
    main_country_number_employees = db.Column(db.Integer, nullable=True)
    other_locations_employees = db.Column(db.String, nullable=True)
    other_locations_employees_html = db.Column(db.String, nullable=True)
    profile_url = db.Column(db.String, index=True)
    homepage_url = db.Column(db.String, index=True, nullable=True)
    timestamp_created = db.Column(db.DateTime, default=func.now(), nullable=True)
    timestamp_updated = db.Column(db.DateTime, onupdate=func.now(), nullable=True)
    jobs = db.relationship('Job', back_populates='company')
    noted_by_user = db.relationship('CompanyUserNote', back_populates='company')

    def __repr__(self):
        return f'<Post {self.name} {self.profile_url}>'


class CompanyUserNote(db.Model):
    __tablename__ = 'CompanyUserNote'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String, nullable=True)
    is_filtered = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())
    is_watched = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User', back_populates='notes_company')

    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    company = db.relationship('Company', back_populates='noted_by_user')




class Job(db.Model):
    __tablename__ = 'Job'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    job_type = db.Column(db.String, nullable=True)
    qualifications = db.Column(db.String, nullable=True)
    salary = db.Column(db.String, nullable=True)
    estimated_salary = db.Column(db.String, nullable=True)
    created_str = db.Column(db.String, nullable=True)  # string of posted ...ago
    _date_posted = db.Column("date_posted", db.Date, nullable=True)
    multiple_candidates = db.Column(db.String, nullable=True)
    benefits = db.Column(db.String, nullable=True)
    description_markdown = db.Column(db.String, nullable=True)
    description_text = db.Column(db.String, nullable=True)
    description_html = db.Column(db.String, nullable=True)
    hiring_insights = db.Column(db.String, nullable=True)
    url = db.Column(db.String, index=True)
    original_url = db.Column(db.String, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'), nullable=True)
    timestamp_created = db.Column(db.DateTime, default=func.now(), nullable=True)
    timestamp_updated = db.Column(db.DateTime, onupdate=func.now(), nullable=True)
    company = db.relationship('Company', back_populates='jobs')
    searches = db.relationship('Search', back_populates='jobs')
    noted_by_user = db.relationship('JobUserNote', back_populates='job')


    @hybrid_property
    def date_posted(self):
        return self._date_posted

    @date_posted.setter
    def date_posted(self, value):
        # value_type = type(value)
        # if value_type != 'str':
        #     print('value_type', value_type, value)
        try:
            self._date_posted = datetime.fromisoformat(value) if value else None
        except ValueError:
            self._date_posted = None

    def __repr__(self):
        return f'<Job {self.date_posted} {self.title} {self.url}>'

class JobUserNote(db.Model):
    __tablename__ = 'JobUserNote'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=True)
    plan_apply_flag = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())
    did_apply_flag = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())
    is_filtered = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())

    job_id = db.Column(db.Integer, db.ForeignKey('Job.id'))
    job = db.relationship('Job', back_populates='noted_by_user')

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User', back_populates='notes_job')


class SearchModel(db.Model):
    __tablename__ = 'SearchModel'
    id = db.Column(db.Integer, primary_key=True)
    what = db.Column(db.String, nullable=True)
    where = db.Column(db.String, nullable=True)
    age = db.Column(db.String, nullable=True)
    radius = db.Column(db.String, nullable=True)
    experience = db.Column(ARRAY(db.String), nullable=True)
    job_category = db.Column(db.Integer, nullable=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())
    searches = db.relationship('Search', back_populates='search_model')

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User', back_populates='search_models')

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, server_default="unnamed")
    linkedin_email = db.Column(db.String, nullable=True)
    linkedin_password = db.Column(db.String,
                                  nullable=True)  # this is for a fake account and need access to the password value
    search_models = db.relationship('SearchModel', back_populates='user')
    notes_company = db.relationship('CompanyUserNote', back_populates='user')
    notes_job = db.relationship('JobUserNote', back_populates='user')


class Search(db.Model):  # junction table Job-SearchModel
    __tablename__ = 'Search'
    id = db.Column(db.Integer, primary_key=True)
    job_board_name = db.Column(db.String)

    job_id = db.Column(db.Integer, db.ForeignKey('Job.id'))
    jobs = db.relationship('Job', back_populates='searches')

    search_model_id = db.Column(db.Integer, db.ForeignKey('SearchModel.id'))
    search_model = db.relationship('SearchModel', back_populates='searches')

    task_id = db.Column(db.String, db.ForeignKey('Task.id'))
    tasks = db.relationship('Task', back_populates='search')


class Task(db.Model):
    __tablename__ = 'Task'
    id = db.Column(db.String, primary_key=True)  # Celery task id
    timestamp = db.Column(db.DateTime(timezone=True), default=db.func.now())
    verification_code = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=True)
    info = db.Column(db.JSON, nullable=True)
    search = db.relationship('Search', back_populates='tasks')
