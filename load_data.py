import os
import sys
import json
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["courses"]
collection = db["courses"]


# read courses from JSON File
def load_courses_data():
    file_path = 'courses.json'
    if not os.path.exists(file_path):
        raise FileNotFoundError("The courses.json file does not exists")
    
    with open(file_path,"r") as f:
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