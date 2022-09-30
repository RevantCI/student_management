CREATE TABLE student
(
 student_id integer,
 student_name varchar(500),
 student_dob  varchar(500),
 student_batchid integer,
 student_marks integer  
);

INSERT INTO student(student_id,student_name,student_dob,student_batchid,student_marks) VALUES (1,'Student 1','18.04.2000',101,30);
INSERT INTO student(student_id,student_name,student_dob,student_batchid,student_marks) VALUES (2,'Student 2','19.05.2001',100,48);
INSERT INTO student(student_id,student_name,student_dob,student_batchid,student_marks) VALUES (3,'Student 3','20.06.2002',101,39);
INSERT INTO student(student_id,student_name,student_dob,student_batchid,student_marks) VALUES (4,'Student 4','21.07.2003',100,3);


CREATE TABLE course
(
 course_id integer,
 course_name varchar(500),
 course_description  varchar(500),
 course_duration integer,
 course_fee integer  
);
INSERT INTO course(course_id,course_name,course_description,course_duration,course_fee) VALUES (100,'Python','Basics',4,20000);
INSERT INTO course(course_id,course_name,course_description,course_duration,course_fee) VALUES (101,'Java','Basics',5,22000);
INSERT INTO course(course_id,course_name,course_description,course_duration,course_fee) VALUES (102,'Python','Intermediate',3,15000);
INSERT INTO course(course_id,course_name,course_description,course_duration,course_fee) VALUES (100,'Python','Advanced',6,30000);



CREATE TABLE batch
(
 batch_id integer,
 course_id integer,
 primary_trainerid integer,
 secondary_trainerid integer,
 batch_startdate varchar(500),
 batch_enddate varchar(500)
 );
INSERT INTO batch(batch_id,course_id,primary_trainerid,secondary_trainerid,batch_startdate,batch_enddate) VALUES (200,100,1000,2000,'01-01-2022','01-06-2022');
INSERT INTO batch(batch_id,course_id,primary_trainerid,secondary_trainerid,batch_startdate,batch_enddate) VALUES (201,101,1001,2000,'06-01-2022','06-06-2022');
INSERT INTO batch(batch_id,course_id,primary_trainerid,secondary_trainerid,batch_startdate,batch_enddate) VALUES (202,100,1002,2002,'07-01-2022','07-06-2022');
INSERT INTO batch(batch_id,course_id,primary_trainerid,secondary_trainerid,batch_startdate,batch_enddate) VALUES (203,102,1000,2001,'08-01-2022','08-06-2022');



CREATE TABLE enrollment
(
 enrollment_id integer,
 student_id integer,
 batch_id integer,
 enrollment_date varchar(500)
);
INSERT INTO enrollment(enrollment_id,student_id,batch_id,enrollment_date) VALUES (10000,100,200,'01-01-2022');
INSERT INTO enrollment(enrollment_id,student_id,batch_id,enrollment_date) VALUES (10001,101,200,'01-01-2022');
INSERT INTO enrollment(enrollment_id,student_id,batch_id,enrollment_date) VALUES (10002,102,201,'01-01-2022');
INSERT INTO enrollment(enrollment_id,student_id,batch_id,enrollment_date) VALUES (10003,103,201,'01-01-2022');

SELECT * FROM student;
DROP TABLE student;

