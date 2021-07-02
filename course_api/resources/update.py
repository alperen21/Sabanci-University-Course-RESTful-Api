from flask_restful import Resource
from flask import request, jsonify
from course_api.common.extract_courses import parse, make_request


class update(Resource):
    def post(self):
        posted_data = request.get_json()
        term = posted_data["term"]
        response = make_request(term)
        parse(response)

        return jsonify ({
            "message":"success"
        })