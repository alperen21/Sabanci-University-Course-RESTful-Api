from flask_restful import Resource
from flask import request
from course_api.common.extract_courses import parse, make_request


class update(Resource):
    def put(self):
        posted_data = request.get_json()
        term = posted_data["term"]
        response = make_request(term)
        parse(response)

        response = {
            "message":"success"
        }

        return response,201