from course_api.database.models import Course, Schedule

def get_crn_with_unique_dates(codes):
    
    uniques = dict()
    result = list()
    for code in codes:
        sections = get_sections(code)[1]

        for section in sections:
            key = str(section["schedule"])
            if key not in uniques:
                uniques[key] = section["crn"]
        
        result.append([ crn for _,crn in uniques.items()])
        uniques = dict()
    
    return result

def crn_to_schedule(crns):
    schedule = list()
    for crn in crns:
        name = Course.query.filter_by(crn=crn).first().name
        classes = Schedule.query.filter_by(crn=crn).all()

        for class_ in classes:
            schedule.append({
                "name":name,
                "day": class_.day,
                "start_time": str(class_.start_time),
                "end_time":str(class_.end_time)
            })
        
    
    return schedule
        

def get_sections(code):
    sections = Course.query.filter_by(code=code).all()

    course_info = list()
    for section in sections:
        crn = section.crn
        schedule = Schedule.query.filter_by(crn = crn).all()
        course_info.append({
            "crn":crn,
            "schedule": [
                {
                    "day":time.day,
                    "start_time":str(time.start_time),
                    "end_time":str(time.end_time)
                } for time in schedule
            ]
        })
    
    return (sections[0].name, course_info)

