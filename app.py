from flask import Flask, request
from flask_restful import Resource, Api
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/courses.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

app = Flask(__name__)
api = Api(app)

db = SQLAlchemy(app)

class course(db.Model):
    name = db.Column(db.String(120), unique=False, nullable=False)
    crn = db.Column(db.String(120), unique=False, nullable=False, primary_key=True)
    code = db.Column(db.String(120), unique=False, nullable=False)

class Hello(Resource):
    def get(self):
        response = {
            "TR": "Merhaba",
            "EN": "Hello,"
        }
        return response, 200

class Course(Resource):
    def get(self,course):
        try:
            mylist = course.split("_")
            mylist[0] = mylist[0].upper()

            parsed_course = mylist[0] + " " + mylist[1]

            return data[parsed_course], 200
            
        except:
            return "error", 201



api.add_resource(Hello,"/")
api.add_resource(Course,"/course/<string:course>")


if __name__ == "__main__":
    app.run(debug=True)