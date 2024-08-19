from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest
from .main import app
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
    
    
    
#     def test_get_all_courses():
# >       response = client.get('/all_courses')
# E       TypeError: 'Database' object is not callable

# test.py:13: TypeError
# ========================================= short test summary info ========================================= 
# FAILED test.py::test_get_all_courses - TypeError: 'Database' object is not callable
# ============================================ 1 failed in 1.48s ============================================ 