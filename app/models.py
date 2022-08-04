from app import db


class Job(db.Model):
    __tablename__='job'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,)
    url = db.Column(db.String, index=True)
    estimated_salary = db.Column(db.String, nullable=True)
    salary = db.Column(db.String, nullable=True)
    job_type = db.Column(db.String, nullable=True)
    multiple_candidates = db.Column(db.String, nullable=True)
    date_posted = db.Column(db.String, nullable=True)
    qualifications = db.Column(db.String, nullable=True)
    benefits = db.Column(db.String, nullable=True)
    description_markdown = db.Column(db.String)
    description_text = db.Column(db.String)
    description_html = db.Column(db.String)
    hiring_insights = db.Column(db.String, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    posts = db.relationship('Company', back_populates='job', lazy='dynamic')


    def __repr__(self):
        return f'<Job {self.title} {self.url}>'

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

class Company(db.Model):
    __tablename__='company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rating = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    profile_url = db.Column(db.String, index=True)
    overview = db.Column(db.String, nullable=True)
    homepage_url = db.Column(db.String, index=True, nullable=True)
    industry = db.Column(db.String, nullable=True)
    size = db.Column(db.String, nullable=True)
    other_locations_employees = db.Column(db.String, nullable=True)
    other_locations_employees_html = db.Column(db.String, nullable=True)
    posts = db.relationship('Job', back_populates='company', lazy='dynamic')


    def __repr__(self):
        return f'<Post {self.name} {self.profile_url}>'


