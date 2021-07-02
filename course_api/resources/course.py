from flask_restful import Resource
from flask import request, jsonify
from course_api.common.util import get_sections
from course_api.database.models import Course


class course(Resource):
    def post(self): #course code to all sections
        posted_data = request.get_json()
        code = posted_data["code"]

        course_name, course_info = get_sections(code)
        
        response = {
            "course_name": course_name,
            "code":code,
            "sections":course_info
        }
        return response, 200
        
    def get(self): #get all courses
        unique = set()
        courses = Course.query.all()

        for course in courses:
            unique.add(course.code)
        unique_list = list(unique)
        unique_list.sort()
        
        response = {
            "courses": unique_list
        }

        return response, 200
