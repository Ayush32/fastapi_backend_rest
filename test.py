from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest
from main import app
from bson import ObjectId
# from httpx import AsyncClient

client = TestClient(app)
print(type(client))


mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['courses']

def test_get_all_courses():
    response = client.get('/all_courses')
    assert response.status_code == 200
    

# @pytest.mark.asyncio
# async def test_get_courses():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/courses")
#     assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_courses_sort_by_alphabetical():
#     async with AsyncClient(app = app,base_url = "http://test") as ac:
#         respone = await ac.get()



mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['courses']


    
#     def test_get_all_courses():
# >       response = client.get('/all_courses')
# E       TypeError: 'Database' object is not callable

def test_get_all_courses():
    response = client.get('/all_courses')
    assert response.status_code == 200

def test_get_courses_sort_by_alphabetical():
    """
    Test the API endpoint for retrieving courses sorted in 
    alphabetical order.

    This test sends a GET request to the '/courses' endpoint 
    with a query parameter 'sort_by' set to 'alphabetical'. 
    It asserts that the response status code is 200, indicating 
    a successful request. It also checks that the response 
    contains a non-empty list of courses and verifies that 
    the courses are sorted by their 'name' attribute in 
    alphabetical order.
    """
    response = client.get('/courses?sort_by=alphabetical')
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0
    assert sorted(courses, key=lambda x: x['name']) == courses
    
    
def test_get_courses_sort_by_date():
    response = client.get('/courses?sort_by=date')
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0
    assert sorted(courses, key=lambda x: x['date'], reverse = True) == courses


def test_get_courses_sort_by_rating():
    response = client.get('/courses?sort_by=rating')
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0
    assert sorted(courses, key=lambda x: x['rating']['total'], reverse = True) == courses


def test_get_courses_sort_by_domain():
    response = client.get('/courses?domain=mathematics')
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0
    assert all([c['domain'][0] == 'mathematics' for c in courses])
    
def test_get_courses_filter_by_domain_and_sort_by_alphabetical():
    response = client.get("/courses?domain=programming&sort_by=alphabetical")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0
    assert all([c['domain'][0] == 'programming' for c in courses])
    assert sorted(courses, key=lambda x: x['name']) == courses

def test_get_course_by_id_exists():
    response = client.get('/courses/66c19cc38937f27e1feab7c9')
    assert response.status_code == 200
    course = response.json()
    # get the courses from database
    course_db = db.courses.find_one({'id' : ObjectId('66c19cc38937f27e1feab7c9')})
    #get the anme of the course from the db
    name_db = course['name']
    name_response = course['name']
    assert name_db == name_response
    
def test_get_course_by_id_not_exists():   
    response = client.get('courses/66c19cc38937f27e6feab7c9')
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Course not found'}     

def test_get_chapter_info():
    response = client.get("/courses/66c19cc38937f27e1feab7ca/1")
    assert response.status_code == 200
    chapter = response.json()
    assert chapter['name'] == 'CS50 2021 in HDR - Lecture 0 - Scratch'
    assert chapter['text'] == 'Introduction to Programming'

def test_get_chapter_info_not_exists():
    response = client.get("/courses/66c19cc38937f27e1feab7ca/990")
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Chapter not found'}   
    
def test_rate_chapter_not_exists():
    response = client.post("/courses/66c19cc38937f27e1feab7ca/990/rate", json={"rating": 1})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
    
#     def test_get_all_courses():
# >       response = client.get('/all_courses')
# E       TypeError: 'Database' object is not callable

# test.py:13: TypeError
# ========================================= short test summary info ========================================= 
# FAILED test.py::test_get_all_courses - TypeError: 'Database' object is not callable
# ============================================ 1 failed in 1.48s ============================================ 