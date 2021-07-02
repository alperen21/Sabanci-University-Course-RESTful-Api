from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from course_api.resources.course import course
from course_api.resources.update import update
from course_api.resources.schedule import schedule
from course_api.resources.hello import Hello

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
api = Api(app)

db = SQLAlchemy(app)      


api.add_resource(Hello,"/")
api.add_resource(update,"/update")
api.add_resource(course,"/course")
api.add_resource(schedule,"/schedule")


if __name__ == "__main__":
    app.run(debug=True)