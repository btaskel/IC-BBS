from exts import db


class Student(db.Model):
    __tablename__ = '_student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.Enum('男', '女', '其他'), nullable=False)
    phone = db.Column(db.String(11))  # 可为空


class Course(db.Model):
    __tablename__ = '_course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    teacher_id = db.Column(db.String(64))


class Teacher(db.Model):
    __tablename__ = '_teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.Enum('男', '女', '其他'), nullable=False)
    phone = db.Column(db.String(11))  # 可为空


class Grade(db.Model):
    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(3), nullable=False)


if __name__ == '__main__':
    s = Student(name='张三', gender='男', phone='11111111111')
    db.session.add(s)
    db.session.commit()
