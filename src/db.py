from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

events_users = db.Table(
    'events_users',
    db.Column('event_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class Event(db.Model):    
    __tablename__ = "course"    
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String, nullable=False)
    assignments = db.relationship("Assignment", cascade="delete", back_populates="course")
    instructors = db.relationship("User", secondary=events_users, back_populates='courses_as_instructor')
    students = db.relationship("User", secondary=events_users, back_populates='courses_as_student')

    def serialize(self):
        return {        
            "id": self.id,        
            "code": self.code,        
            "name": self.name, 
            "assignments": [a.serialize() for a in self.assignments], 
            "instructors": [i.serialize_without_courses() for i in self.instructors],   
            "students": [s.serialize_without_courses() for s in self.students]
        }

class User(db.Model):
    __tablename__ = "user"    
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    courses_as_student = db.relationship("Course", secondary=course_students, back_populates='students')
    courses_as_instructor = db.relationship("Course", secondary=course_instructors, back_populates='instructors')


    def serialize(self):    
        return {        
            "id": self.id,        
            "name": self.name,
            "netid": self.netid,
            "courses": [s.serialize() for s in self.courses_as_student] + [i.serialize() for i in self.courses_as_instructor]
        }