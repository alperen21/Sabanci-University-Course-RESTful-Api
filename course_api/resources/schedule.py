from flask_restful import Resource
from flask import request, jsonify
from course_api.common.util import get_crn_with_unique_dates, crn_to_schedule
import itertools


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