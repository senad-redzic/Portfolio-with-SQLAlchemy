from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    short_description = db.Column(db.String(400))
    skills = db.Column(db.String(120))
    date = db.Column(db.Date)
    github_link = db.Column(db.String(120))

    def __init__(self, title, date, skills, short_description, github_link):
        self.title = title
        self.date = date
        self.skills = skills
        self.short_description = short_description
        self.github_link = github_link

    def __repr__(self):
        return f'<Project {self.title}>'
