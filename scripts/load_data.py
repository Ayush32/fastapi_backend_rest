import os
import sys
import json
import pymongo

# Adjust sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import collection, client

# read courses from JSON File
def load_courses_data():
    if not os.path.exists("app/courses.json"):
        raise FileNotFoundError("The courses.json file does not exists")
    
    with open("app/courses.json","r") as f:
        courses = json.load(f)
        
    # create index for efficient retrieval
    collection.create_index("name")
    
    # add rating field to each courses
    for course in courses:
        course['rating'] = {'total' : 0,
                            'count' : 0}
    
    # add rating filed to each chapter
    for course in courses:
        for chapter in course['chapters']:
            chapter['rating'] = {'total' : 0, 'count' : 0}
    
    
# add course data into collection        
    for course in courses:
        collection.insert_one(course)



if __name__ == "__main__":
    load_courses_data()
    print("Course data added successfully")
    
client.close()
    
#  File "C:\Users\721ay\OneDrive\Desktop\fastapi-mongo\scripts\load_data.py", line 3, in <module>
#     from ..app.database  import sync_collection, setup_indices
# ImportError: attempted relative import with no known parent package