from app import db
from sqlalchemy.sql import expression


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rating = db.Column(db.String, nullable=True)
    industry = db.Column(db.String, nullable=True)
    size = db.Column(db.String, nullable=True)
    overview = db.Column(db.String, nullable=True)
    number_employees = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    main_country_name = db.Column(db.String, nullable=True)
    main_country_number_employees = db.Column(db.String, nullable=True)
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
    created_str = db.Column(db.String, nullable=True) # string of posted ...ago
    date_posted = db.Column(db.String, nullable=True)
    multiple_candidates = db.Column(db.String, nullable=True)
    benefits = db.Column(db.String, nullable=True)
    description_markdown = db.Column(db.String)
    description_text = db.Column(db.String)
    description_html = db.Column(db.String)
    hiring_insights = db.Column(db.String, nullable=True)
    url = db.Column(db.String, index=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false())
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    company = db.relationship('Company', back_populates='jobs')

    def __repr__(self):
        return f'<Job {self.title} {self.url}>'

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)