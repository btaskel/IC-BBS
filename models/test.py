from exts import db


# class pop(db):
#     __tablename__ = 'pop'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#
# class pop_teacher(db):
#     __tablename__ = 'pop_teacher'
#     id = db.Column(db.integer, primary_key=True)
#     name = db.Column(db.String(50),nullable=False)
#
# class pop_score(db):

association_table = db.Table('association',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


# 定义 Student 模型
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    courses = db.relationship('Course', secondary=association_table, back_populates='students')

# 定义 Course 模型
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    students = db.relationship('Student', secondary=association_table, back_populates='courses')











