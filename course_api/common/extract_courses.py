#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import re
import sys
from datetime import datetime
from sqlalchemy import Column, Integer, String,create_engine, ForeignKey, Time
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text
from datetime import date

engine = create_engine('sqlite:///courses.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)



class Course(Base):
    __tablename__="Course"
    name = Column(String)
    crn = Column(String, primary_key=True)
    code = Column(String)

class Schedule(Base):
    __tablename__="Schedule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    crn = Column(String, ForeignKey('Course.crn'))
    day = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)


def truncate_all_tables():
    with engine.connect() as con:
        statement=text(""" 
        DELETE FROM Schedule WHERE 1=1;
        """)
        con.execute(statement)

        statement=text(""" 
        DELETE FROM Course WHERE 1=1;
        """)
        con.execute(statement)

def guess_crn(course_string):
    course_parsed = course_string.split(" - ")
    course_parsed = [x.strip() for x in course_parsed]
    name = course_parsed[0].strip()

    i = 1
    hashmap = dict()
    hashmap[0] = True
    crn = str()
    while(i < len(course_parsed)):
        if (course_parsed[i].isdecimal()):
            #found the crn
            crn = course_parsed[i]
            hashmap[i] = True
            break
        i+=1
    keys = list(hashmap.keys())
    for i in range(4):
        if (i not in keys and len(course_parsed[i])> 3):
            code = course_parsed[i]
    return (name, code, crn)


def make_request(term):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://suis.sabanciuniv.edu',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://suis.sabanciuniv.edu/prod/bwckgens.p_proc_term_date',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = [
    ('term_in', term),
    ('sel_subj', 'dummy'),
    ('sel_subj', 'AL'),
    ('sel_subj', 'ACC'),
    ('sel_subj', 'CS'),
    ('sel_subj', 'CULT'),
    ('sel_subj', 'DA'),
    ('sel_subj', 'ECON'),
    ('sel_subj', 'ETM'),
    ('sel_subj', 'ENS'),
    ('sel_subj', 'ENG'),
    ('sel_subj', 'FIN'),
    ('sel_subj', 'HART'),
    ('sel_subj', 'HIST'),
    ('sel_subj', 'HUM'),
    ('sel_subj', 'IE'),
    ('sel_subj', 'IT'),
    ('sel_subj', 'IF'),
    ('sel_subj', 'IR'),
    ('sel_subj', 'MGMT'),
    ('sel_subj', 'MKTG'),
    ('sel_subj', 'MAT'),
    ('sel_subj', 'MATH'),
    ('sel_subj', 'ME'),
    ('sel_subj', 'NS'),
    ('sel_subj', 'OPIM'),
    ('sel_subj', 'PROJ'),
    ('sel_subj', 'SEC'),
    ('sel_subj', 'SPS'),
    ('sel_subj', 'SOC'),
    ('sel_subj', 'TLL'),
    ('sel_subj', 'TS'),
    ('sel_day', 'dummy'),
    ('sel_schd', 'dummy'),
    ('sel_insm', 'dummy'),
    ('sel_camp', 'dummy'),
    ('sel_levl', 'dummy'),
    ('sel_sess', 'dummy'),
    ('sel_instr', 'dummy'),
    ('sel_ptrm', 'dummy'),
    ('sel_attr', 'dummy'),
    ('sel_crse', ''),
    ('sel_title', ''),
    ('sel_from_cred', ''),
    ('sel_to_cred', ''),
    ('begin_hh', '0'),
    ('begin_mi', '0'),
    ('begin_ap', 'a'),
    ('end_hh', '0'),
    ('end_mi', '0'),
    ('end_ap', 'a'),
    ]

    response = requests.post('https://suis.sabanciuniv.edu/prod/bwckschd.p_get_crse_unsec', headers=headers, data=data)

    return response

def parse(response):
    truncate_all_tables()
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all(class_="ddlabel")

    courses = list()
    for result in results:
        courses.append(result.text)


    results = soup.find_all("table", summary="This table lists the scheduled meeting times and assigned instructors for this class..")
    count = 0
    schedules = list()
    for result in results:
        pattern = "[0-9]?[0-9]:[0-9][0-9] .. - [0-9]?[0-9]:[0-9][0-9] ..\n."
        times = re.findall(pattern, result.text)
        schedules.append(times)
        #schedules.append(result)

    
    session = Session()
    for course_string, schedule in zip(courses, schedules):


        course_parsed = course_string.split(" - ")
        name = course_parsed[0].strip()
        if ("Lab" in course_string or "Recitation" in course_string or "Discussion" in course_string):
            crn = course_parsed[2].strip()
            code = course_parsed[3].strip()
            name += " recit."
        else:
            crn = course_parsed[1].strip()
            code = course_parsed[2].strip()
            name += " recit."
        
        if (crn.isdecimal() == False):
            mytuple = guess_crn(course_string)
            name = mytuple[0]
            name += " (?)"
            code = mytuple[1]
            crn = mytuple[2]
        
        course = Course()
        course.name = name
        course.crn = crn
        course.code = code

        print(crn)
        

        session.add(course)

        for time in schedule:
            parsed = time.split("\n")
            day = parsed[1]
            start_time_string = parsed[0].split(" - ")[0]
            end_time_string = parsed[0].split(" - ")[1]

            format = "%I:%M %p"

            start_time = datetime.strptime(start_time_string, format).time()
            end_time = datetime.strptime(end_time_string, format).time()

            
            schedule = Schedule()
            schedule.crn = crn
            schedule.day = day
            schedule.start_time = start_time
            schedule.end_time = end_time

            session.add(schedule)

        session.commit()
        
        

    session.close()
            
        
if __name__ == "__main__":
    
    if (len(sys.argv) < 3):
        print("not enough arguments are given")
        sys.exit(1)

    term_to_number = {
        "fall":"01",
        "spring":"02",
        "summer":"03",
        "01":"01",
        "02":"02",
        "03":"03"
    }

    try:
        term = term_to_number[sys.argv[1].lower()]
        year = sys.argv[2]
    except Exception:
        print("invalid term argument")
        sys.exit(1)
    
    if ((not year.isdecimal()) or (int(year) < 2000) or (int(year) > date.today().year)):
        print("invalid year argument")
        sys.exit(1)
    
    try:
        print("request is being sent to the server")
        response = make_request(year+term)
        print("response has been received")
        print("parsing information")
        parse(response)
        print("done!")
        sys.exit(0)
    except Exception as e:
        print("something went wrong...")
        print(e)