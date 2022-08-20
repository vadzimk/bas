from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from . import db
from sqlalchemy.sql import expression


class Company(db.Model):
    __tablename__ = 'company'
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
    jobs = db.relationship('Job', back_populates='company')

    def __repr__(self):
        return f'<Post {self.name} {self.profile_url}>'


class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, )
    job_type = db.Column(db.String, nullable=True)
    qualifications = db.Column(db.String, nullable=True)
    salary = db.Column(db.String, nullable=True)
    estimated_salary = db.Column(db.String, nullable=True)
    created_str = db.Column(db.String, nullable=True)  # string of posted ...ago
    _date_posted = db.Column("date_posted", db.Date, nullable=True)
    multiple_candidates = db.Column(db.String, nullable=True)
    benefits = db.Column(db.String, nullable=True)
    description_markdown = db.Column(db.String)
    description_text = db.Column(db.String)
    description_html = db.Column(db.String)
    hiring_insights = db.Column(db.String, nullable=True)
    url = db.Column(db.String, index=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())
    plan_apply_flag = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())
    did_apply_flag = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())
    note = db.Column(db.Text, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    company = db.relationship('Company', back_populates='jobs')

    @hybrid_property
    def date_posted(self):
        return self._date_posted

    @date_posted.setter
    def date_posted(self, value):
        value_type = type(value)
        if value_type != 'str':
            print('value_type', value_type, value)
        self._date_posted = datetime.fromisoformat(value) if value else None





    def __repr__(self):
        return f'<Job {self.date_posted} {self.title} {self.url}>'


