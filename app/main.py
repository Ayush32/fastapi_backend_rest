from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
import contextlib
from typing import Optional

app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')
db = client['courses']

# function to get the chapter - DRY 
def get_chapter(chapters, chapter_id: str):
    """Retrieve a chapter by its index."""
    try:
        chapter_index = int(chapter_id)
        if chapter_index < 0 or chapter_index >= len(chapters):
            raise IndexError("Chapter index out of range")
        return chapters[chapter_index]
    except (ValueError, IndexError):
        raise HTTPException(status_code=404, detail='Chapter not found') from e

#  Fetch the course document from the database.
def fetch_course(course_id : str):
    # The ObjectId is used to convert the string course_id to a MongoDB ObjectId
    course = db.courses.find_one({'_id' : ObjectId(course_id)},{'_id' : 0, })
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    
    return course


@app.get('/all_courses')
def get_all_courses():
    courses = db.courses.find()
    # Convert the cursor to a list and replace ObjectId with string
    courses_list = []
    for course in courses:
        course['_id'] = str(course['_id'])  # Convert ObjectId to string
        courses_list.append(course)
    return courses_list

# All available course based on the query parameter like sorting domain
# @app.get('/courses')
# def get_course(sort_by : str = 'date',domain : str = None):
    
#     for course in db.courses.find():
#         total = 0
#         count = 0
#         for chapter in course['chapters']:
#             with contextlib.suppress(KeyError):
#                 total += chapter['rating']['total']
#                 count += chapter['rating']['count']
#         db.courses.update_one({'_id' : course['_id']},{'$set' : {'rating' : {'total' : total, 'count' : count}}})

#      # sort_by = 'date'[DESCENDING]
#     if sort_by == 'date':
#         sort_field = 'date'
#         sort_order = -1 
    
#      # sort_by = 'rating'[DESCENDING]
#     elif sort_by == 'rating':
#         sort_field = 'rating.total'
#         sort_order = -1
    
#     # sort_by = alphabeticl[ASCENDING]
#     else:
#         sort_field = 'name'
#         sort_order = 1
    
#     query = {}
#     if domain:
#         query['doamin'] = domain
    
#     courses = db.courses.find(query, {'name' : 1,'date' : 1,'description' : 1,'domain' : 1, 'rating' : 1,'_id' : 0}).sort(sort_field,sort_order)
#     return list(courses)    


@app.get('/courses')
def get_course(sort_by: str = Query('date', enum=['date', 'rating', 'alphabetical']), domain: str = None):
    """
    Fetch courses from the database, optionally sorting and filtering by domain.
    
    Parameters:
    - sort_by: The field to sort the courses by (date, rating, or alphabetical).
    - domain: Optional filter to return courses belonging to a specific domain.
    """
    # Update ratings for each course
    for course in db.courses.find():
        total_rating = sum(chapter.get('rating', {}).get('total', 0) for chapter in course.get('chapters', []))
        count_rating = sum(chapter.get('rating', {}).get('count', 0) for chapter in course.get('chapters', []))
        
        # Update the course rating in the database
        db.courses.update_one(
            {'_id': course['_id']},
            {'$set': {'rating': {'total': total_rating, 'count': count_rating}}}
        )

    # Determine sorting parameters based on the sort_by argument
    sort_field, sort_order = {
        'date': ('date', -1),
        'rating': ('rating.total', -1),
        'alphabetical': ('name', 1)
    }.get(sort_by, ('date', -1))  # Default to sorting by date if invalid sort_by

    # Build the query for filtering by domain
    query = {}
    if domain:
        query['domain'] = domain  # Fixed typo from 'doamin' to 'domain'

    # Fetch and sort courses from the database
    courses = db.courses.find(query, {
        'name': 1,
        'date': 1,
        'description': 1,
        'domain': 1,
        'rating': 1,
        '_id': 0
    }).sort(sort_field, sort_order)

    return list(courses)

    
    
"""
    Retrieve a course by its name from the database.
    Args:
        course_name (str): The name of the course to retrieve.
    Returns:
        dict: A dictionary containing the course details.
    Raises:
        HTTPException: If the course is not found in the database.
    """
    
@app.get('/courses/{course_id}')
def get_course_by_id(course_id : str):
    
    # Fetch the course document with par from the database
    course = db.courses.find_one({'_id' : ObjectId(course_id)}, {'_id': 0, 'chapters': 0})
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    
     # Convert ObjectId to string
    # course['_id'] = str(course['_id']) 
    try:
        course['rating'] = course['rating']['total']
    except KeyError:
        course['rating'] = 'Not rated yet'
        
    return course



@app.get('/courses/{course_id}/{chapter_id}')
def get_chapter_details(course_id : str, chapter_id : str):
    
    # Fetch the course document from the database
    course = fetch_course(course_id)
    
    # Retrieve the list of chapters from the course document
    # If 'chapters' does not exist, default to an empty list
    chapters = course.get('chapters',[])
    
    # print(f"Chapters: {chapters}")  # You can replace this with a proper logging mechanism
    
     # Check if the chapter_id is a valid integer and within range
    chapter = get_chapter(chapters,chapter_id)

    return chapter

@app.post('/courses/{course_id}/{chapter_id}')
def rate_chapter(course_id : str, chapter_id : str, rating: int = Query(..., gt=-2, lt=2)):
    # Fetch the course document from the database
    course = fetch_course(course_id)
    
    # Retrieve the list of chapters from the course document
    # If 'chapters' does not exist, default to an empty list
    chapters = course.get('chapters',[])
    
    # Retrieve the chapter 
    chapter = get_chapter(chapters, chapter_id)
    
    try:
        # If the chapter already has a rating, update the total and count
        chapter['rating']['total'] += rating
        chapter['rating']['count'] += 1
    except KeyError:
        # If the chapter does not have a rating, initialize the rating
        chapter['rating'] = {'total' : rating, 'count' : 1}
    
     # Update the course document in the database with the new rating
    db.courses.update_one({'_id' : ObjectId(course_id)}, {'$set' : {'chapters' : chapters}})
    
    return chapter
