from flask_restful import Resource

class Hello(Resource):
    def get(self):
        response = {
            "TR": "Merhaba",
            "EN": "Hello,"
        }
        return response, 200