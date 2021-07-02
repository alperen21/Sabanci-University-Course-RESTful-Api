from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Course(db.Model):
    name = db.Column(db.String)
    crn = db.Column(db.String, primary_key=True)
    code = db.Column(db.String)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crn = db.Column(db.String, db.ForeignKey('Course.crn'))
    day = db.Column(db.String)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)