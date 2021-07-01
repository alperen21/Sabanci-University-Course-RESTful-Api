from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
import itertools
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from extract_courses import parse, make_request

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

def get_crn_with_unique_dates(codes):
    
    uniques = dict()
    result = list()
    for code in codes:
        sections = get_sections(code)[1]

        for section in sections:
            key = str(section["schedule"])
            if key not in uniques:
                uniques[key] = section["crn"]
        
        result.append([ crn for _,crn in uniques.items()])
        uniques = dict()
    
    return result

def crn_to_schedule(crns):
    schedule = list()
    for crn in crns:
        name = Course.query.filter_by(crn=crn).first().name
        classes = Schedule.query.filter_by(crn=crn).all()

        for class_ in classes:
            schedule.append({
                "name":name,
                "day": class_.day,
                "start_time": str(class_.start_time),
                "end_time":str(class_.end_time)
            })
        
    
    return schedule
        

def get_sections(code):
    sections = Course.query.filter_by(code=code).all()

    if (len(sections) == 0):
        return jsonify({
            "message":"course not found"
        })

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
    
    return (sections[0].name, course_info)


class course(Resource):
    def post(self): #course code to all sections
        posted_data = request.get_json()
        code = posted_data["code"]

        course_name, course_info = get_sections(code)
        
        return jsonify ({
            "course_name": course_name,
            "code":code,
            "sections":course_info
        })


class schedule(Resource):
    def post(self):
        posted_data = request.get_json()
        print(posted_data)
        codes = posted_data["codes"] #should be a list of course codes
        grouped_crns = get_crn_with_unique_dates(codes)
        
        crn_combinations = list(itertools.product(*grouped_crns))
        schedules = [crn_to_schedule(crn) for crn in crn_combinations]
        

        return jsonify({
            "schedules":schedules
        })
            
class update(Resource):
    def post(self):
        posted_data = request.get_json()
        term = posted_data["term"]
        response = make_request(term)
        parse(response)

        return jsonify ({
            "message":"success"
        })

api.add_resource(Hello,"/")
api.add_resource(update,"/update")
api.add_resource(course,"/course")
api.add_resource(schedule,"/schedule")


if __name__ == "__main__":
    app.run(debug=True)