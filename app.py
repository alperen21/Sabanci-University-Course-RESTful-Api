from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
api = Api(app)

db = SQLAlchemy(app)


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

class Hello(Resource):
    def get(self):
        response = {
            "TR": "Merhaba",
            "EN": "Hello,"
        }
        return response, 200

class course(Resource):
    def post(self): #course code to all sections
        posted_data = request.get_json()
        code = posted_data["code"]

        sections = Course.query.filter_by(code=code).all()

        course_info = list()
        for section in sections:
            crn = section.crn
            schedule = Schedule.query.filter_by(crn = crn).all()
            course_info.append({
                "crn":crn,
                "schedule": [
                    {
                        "day":time.day,
                        "start_time":str(time.start_time),
                        "end_time":str(time.end_time)
                    } for time in schedule
                ]
            })
        
        return jsonify ({
            "course_name": sections[0].name,
            "code":code,
            "sections":course_info
        })
            



api.add_resource(Hello,"/")
api.add_resource(course,"/course")


if __name__ == "__main__":
    app.run(debug=True)