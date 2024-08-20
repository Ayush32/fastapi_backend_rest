Completed Assessment for Kimo using FastAPI and MongoDb.

## clone the Repository using git clone 
* https://github.com/Ayush32/fastapi_backend_rest
* Open the directory in vscode
* run virutalenv venv
* activate the virtualenv - venv/ascripts/activate
* go back to root directory
* run fastapi dev main.py

## Running Tests
```py
pytest test.py
```
# Adding the Collection to MongoDB
```py
python load_data.py
```
### Adding the courses.json to MongoDB using the Python script
![ss1](https://github.com/user-attachments/assets/ff0ccc6b-52df-43a1-98d9-67d736d09509)

### Courses Endpoint
Get all the courses with chapter
* http://127.0.0.1:8000/all_courses
![ss2](https://github.com/user-attachments/assets/55469752-5fd8-4253-a5b6-8d4d9d1a118a)

### Single Course Endpoint using id
* http://127.0.0.1:8000/courses/{course_id}
![ss3](https://github.com/user-attachments/assets/aebdddf4-70c6-44b8-bb48-ef3132e22c10)

### Get the course in sorted order by date
* http://127.0.0.1:8000/courses?sort_by=date
![ss4](https://github.com/user-attachments/assets/0cf7c283-7bce-41dd-b45b-343e8ce0f1af)

### Get the course in sorted order by alphabetical
* http://127.0.0.1:8000/courses?sort_by=alphabetical
![ss5](https://github.com/user-attachments/assets/2ba776a6-b988-404f-89bb-4d877813c878)

### Get the course in sorted order by rating
* http://127.0.0.1:8000/courses?sort_by=rating
![ss6](https://github.com/user-attachments/assets/8bb855c9-07b3-4ce3-baa3-6c81cb7aafee)

### Chapter Details Endpoint
* http://127.0.0.1:8000/courses/{course_id}/{chapter_id}
![ss7](https://github.com/user-attachments/assets/fcd4216c-9d08-4429-88f1-4dcf376800c4)

### POST Request Endpoint to add rating to a Chapter
* http://127.0.0.1:8000/courses/66c4753edcd98a1610b92966/2?rating=1
![ss8](https://github.com/user-attachments/assets/dd021996-6ecd-425c-a4a3-8de6eab5b78e)
* Success
![ss9](https://github.com/user-attachments/assets/ded1f6b6-278a-4155-91b3-bc21c467544a)

### Running Tests to validate all endpoints
![ss10](https://github.com/user-attachments/assets/d645032f-dceb-4953-9914-ae73c657d187)

### dockerizing fastapi application
![ss11](https://github.com/user-attachments/assets/42b1e4d6-8399-4cbf-b04d-36f1020417e8)

