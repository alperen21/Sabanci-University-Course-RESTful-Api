from flask import Flask, request
from flask_restful import Resource, Api
import json

with open("course_data.json","r") as json_file:
    data = json.load(json_file)
    

app = Flask(__name__)
api = Api(app)

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