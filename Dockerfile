FROM python:3.9-alpine
WORKDIR /Sabanci-University-Course-RESTful-Api
ADD . /Sabanci-University-Course-RESTful-Api
RUN  apk add build-base
RUN pip install -r requirements.txt
ENV FLASK_APP "course_api/app.py"
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]