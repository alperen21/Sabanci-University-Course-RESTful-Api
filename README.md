# Flask-RESTful Api for Sabanci University Courses



### Background
Hello,

  I am a rising Sophomore Computer Science student. This project was created as a precursor to another, project. I had to scrape course data from the website of the university but due to dynamic nature of the website, it was very challenging for me to extract information from the website. Because of that, I decided to create a RESTful Api to help other novice computer science students who want to develop projects about offered courses so that they do not have to scrape the data themselves.

  The information is stored within a JSON file and Rest Api serves the portion of the data the user needs. The project has been developed with a custom scraping algorithm I wrote and the api is written using Flask-Restful. The active api can be accessed here http://sabancicourseapi.pythonanywhere.com/
  
### How To Use The API?

  Homepage of the url will return a "hello json" file. In order to access the data use url end point template course/course_name. This will return a JSON file that can be easily converted into a nested list. The list will contain several other list, each list symbolizes a section. Each section list will also contain several dictionaries, each dictionary corresponds to one lecture block / hour except the last one, the last dictionary always corresponds to CRN of that section. for example, if a course has 2 lectures on monday and tuesday, the list will contain three dictionaries: the first one corresponds to the monday lecture, the second one corresponds to the tuesday lecture and the third and final one will contain the CRN. Each lecture dictionary contains information about the hour and the day in which the lecture will take place.
  
 ### Example
  
  For example, in order to access information about class IF 100, one must follow the link: http://sabancicourseapi.pythonanywhere.com/course/cs_201
 As you can see the JSON response Looks like this:
  
  [[{"day": "M", "time": "8:40 am - 10:30 am"}, {"day": "W", "time": "12:40 pm - 1:30 pm"}, {"crn": "10152"}], [{"day": "M", "time": "1:40 pm - 3:30 pm"}, {"day": "W", "time": "4:40 pm - 5:30 pm"}, {"crn": "10153"}]]
  
  The response contains two lists, which means this particular course contains 2 sections.
  
 [{"day": "M", "time": "8:40 am - 10:30 am"}, {"day": "W", "time": "12:40 pm - 1:30 pm"}, {"crn": "10152"}]
 [{"day": "M", "time": "1:40 pm - 3:30 pm"}, {"day": "W", "time": "4:40 pm - 5:30 pm"}, {"crn": "10153"}]
  
  Let's focus on the first section. The list that corresponds to the first section has 3 elements:
  
  {"day": "M", "time": "8:40 am - 10:30 am"}
  {"day": "W", "time": "12:40 pm - 1:30 pm"}
  {"crn": "10152"}
  
  That means, each student will need to attend lectures on Monday 8:40 - 10:30 and Wednesday 12:40 - 13:30. Third dictionary contains the crn code, so in order to register for this section the students have to use this particular code. The information can be accessed by using keys. I did not implement location information because of the proximity of faculties with each other.
