from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import databases
import aiosqlite
import sqlalchemy


DATABASE_URL = "sqlite:///./student.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

student = sqlalchemy.Table(
    "student",
    metadata, 
    sqlalchemy.Column("student_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("student_name", sqlalchemy.String(500)),
    sqlalchemy.Column("student_dob", sqlalchemy.String(500)),
    sqlalchemy.Column("student_batchid", sqlalchemy.Integer),
    sqlalchemy.Column("student_marks", sqlalchemy.Integer)
)

course = sqlalchemy.Table(
    "course",
    metadata, 
    sqlalchemy.Column("course_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("course_name", sqlalchemy.String(500)),
    sqlalchemy.Column("course_description", sqlalchemy.String(500)),
    sqlalchemy.Column("course_duration", sqlalchemy.Integer),
    sqlalchemy.Column("course_fee", sqlalchemy.Integer)
)

batch = sqlalchemy.Table(
    "batch",
    metadata, 
    sqlalchemy.Column("batch_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("course_id", sqlalchemy.Integer),
    sqlalchemy.Column("primary_trainerid", sqlalchemy.Integer),
    sqlalchemy.Column("secondary_trainerid", sqlalchemy.Integer),
    sqlalchemy.Column("batch_startdate", sqlalchemy.String(500)),
    sqlalchemy.Column("batch_enddate", sqlalchemy.String(500))
)

enrollment = sqlalchemy.Table(
    "enrollment",
    metadata, 
    sqlalchemy.Column("enrollment_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("student_id", sqlalchemy.Integer),
    sqlalchemy.Column("batch_id", sqlalchemy.Integer),
    sqlalchemy.Column("enrollment_date", sqlalchemy.String(500))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

####################### STUDENT ############################################

class StudentIn(BaseModel):
    student_name: str
    student_dob: str
    student_batchid : int
    student_marks   : int

class Student(BaseModel):
    student_id      : int
    student_name    : str
    student_dob     : str
    student_batchid : int
    student_marks   : int

@app.post('/addstudent/', response_model=Student)
async def addstudent(r: StudentIn = Depends()):
    query = student.insert().values(
        student_name    = r.student_name,
        student_dob     = r.student_dob,
        student_batchid = r.student_batchid,
        student_marks   = r.student_marks
    )
    student_id = await database.execute(query)
    query = student.select().where(student.c.student_id == student_id)
    row = await database.fetch_one(query)
    return {**row}

@app.get('/getstudent/{student_id}', response_model=Student)
async def get_student(student_id: int):
    query = student.select().where(student.c.student_id == student_id)
    one_student = await database.fetch_one(query)
    return {**one_student}

@app.get('/getstudents/', response_model=List[Student])
async def get_students():
    query = student.select()
    students = await database.fetch_all(query)
    return students

@app.put('/updatestudent/{student_id}', response_model=Student)
async def update_student(student_id: int, r: StudentIn = Depends()):

    query = student.update().where(student.c.student_id == student_id).values(
        student_name=r.student_name,
        student_dob     = r.student_dob,
        student_batchid = r.student_batchid,
        student_marks   = r.student_marks
        
    )
    student_id = await database.execute(query)
    query = student.select().where(student.c.student_id == student_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/deletestudent/{student_id}", response_model=Student)
async def delete_student(student_id: int):
    query = student.delete().where(student.c.student_id == student_id)
    return await database.execute(query)

###################################### COURSE #################################
class UpdateCourse(BaseModel):
    course_name         : str
    course_description  : str
    course_duration     : int    
    course_fee          : int

class Course(BaseModel):

    course_id           : int 
    course_name         : str
    course_description  : str
    course_duration     : int    
    course_fee          : int
@app.post('/addcourse/', response_model=Course)
async def add_course(r: UpdateCourse = Depends()):
    query = course.insert().values(

    course_name         = r.course_name,
    course_description  = r.course_description,
    course_duration     = r.course_duration,
    course_fee          = r.course_fee
    )
    course_id = await database.execute(query)
    query = course.select().where(course.c.course_id == course_id)
    row = await database.fetch_one(query)
    return {**row}

@app.get('/getcourse/{course_id}', response_model=Course)
async def get_course(course_id: int):
    query = course.select().where(course.c.course_id == course_id)
    one_course = await database.fetch_one(query)
    return {**one_course}

@app.get('/getcourses/', response_model=List[Course])
async def get_courses():
    query = course.select()
    courses = await database.fetch_all(query)
    return courses

@app.put('/updatecourse/{course_id}', response_model=Course)
async def update_course(course_id: int, r: UpdateCourse = Depends()):

    query = course.update().where(course.c.course_id == course_id).values(
    course_name         = r.course_name,
    course_description  = r.course_description,
    course_duration     = r.course_duration,
    course_fee          = r.course_fee
        
    )
    course_id = await database.execute(query)
    query = course.select().where(course.c.course_id == course_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/deletecourse/{course_id}", response_model=Course)
async def delete_course(course_id: int):
    query = course.delete().where(course.c.course_id == course_id)
    return await database.execute(query)
###################################### BATCH #################################
class UpdateBatch(BaseModel):
    course_id               : int
    primary_trainerid       : int
    secondary_trainerid     : int
    batch_startdate         : str
    batch_enddate           : str

class Batch(BaseModel):
    batch_id                : int
    course_id               : int
    primary_trainerid       : int
    secondary_trainerid     : int
    batch_startdate         : str
    batch_enddate           : str
@app.post('/addbatch/', response_model=Batch)
async def addbatch(r: UpdateBatch = Depends()):
    query = batch.insert().values(

    course_id           = r.course_id,
    primary_trainerid   = r.primary_trainerid,
    secondary_trainerid = r.secondary_trainerid,
    batch_startdate     = r.batch_startdate,
    batch_enddate     = r.batch_enddate
    )
    batch_id = await database.execute(query)
    query = batch.select().where(batch.c.batch_id == batch_id)
    row = await database.fetch_one(query)
    return {**row}

@app.get('/getbatches/', response_model=List[Batch])
async def get_batches():
    query = batch.select()
    batches = await database.fetch_all(query)
    return batches

@app.put('/updatebatch/{batch_id}', response_model=Batch)
async def updatebatch(batch_id: int, r: UpdateBatch = Depends()):

    query = batch.update().where(batch.c.batch_id == batch_id).values(
    course_id           = r.course_id,
    primary_trainerid   = r.primary_trainerid,
    secondary_trainerid = r.secondary_trainerid,
    batch_startdate     = r.batch_startdate,
    batch_enddate     = r.batch_enddate
        
    )
    batch_id = await database.execute(query)
    query = batch.select().where(batch.c.batch_id == batch_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/deletebatch/{batch_id}", response_model=Batch)
async def deletebatch(batch_id: int):
    query = batch.delete().where(batch.c.batch_id == batch_id)
    return await database.execute(query)

################################ENROLLMENT #################################
class UpdateEnrollment(BaseModel):
    student_id         : int
    batch_id           : int
    enrollment_date    : str

class Enrollment(BaseModel):
    enrollment_id      : int
    student_id         : int
    batch_id           : int
    enrollment_date    : str

@app.post('/addenrollment/', response_model=Enrollment)
async def add_enrollment(r: UpdateEnrollment = Depends()):
    query = enrollment.insert().values(

    student_id       = r.student_id,
    batch_id         = r.batch_id,
    enrollment_date  = r.enrollment_date
 )
    enrollment_id = await database.execute(query)
    query = enrollment.select().where(enrollment.c.enrollment_id == enrollment_id)
    row = await database.fetch_one(query)
    return {**row}

@app.get('/getenrollments/', response_model=List[Enrollment])
async def get_enrollments():
    query = enrollment.select()
    enrollments = await database.fetch_all(query)
    return enrollments

@app.put('/updateenrollment/{enrollment_id}', response_model=Enrollment)
async def update_enrollment(enrollment_id: int, r: UpdateEnrollment = Depends()):

    query = enrollment.update().where(enrollment.c.enrollment_id == enrollment_id).values(
    student_id       = r.student_id,
    batch_id         = r.batch_id,
    enrollment_date  = r.enrollment_date
        
    )
    enrollment_id = await database.execute(query)
    query = enrollment.select().where(enrollment.c.enrollment_id == enrollment_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/deleteenrollment/{enrollment_id}", response_model=Enrollment)
async def delete_enrollment(enrollment_id: int):
    query = enrollment.delete().where(enrollment.c.enrollment_id == enrollment_id)
    return await database.execute(query)
    
    