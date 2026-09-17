from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='student')
    class_group_id = db.Column(db.Integer, db.ForeignKey('class_group.id'))
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
    @property
    def is_admin(self): return self.role == 'admin'

class ClassGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    profile = db.Column(db.String(100), default='Общеобразовательный')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), default='#6c63ff')

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    building = db.Column(db.String(80), default='Главный корпус')

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.Integer, nullable=False)
    lesson_number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    class_group_id = db.Column(db.Integer, db.ForeignKey('class_group.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    class_group = db.relationship('ClassGroup')
    teacher = db.relationship('Teacher')
    subject = db.relationship('Subject')
    classroom = db.relationship('Classroom')

@login_manager.user_loader
def load_user(user_id): return db.session.get(User, int(user_id))

def seed_data():
    if User.query.first(): return
    group = ClassGroup(name='10А', profile='Физико-математический')
    db.session.add(group)
    teacher = Teacher(full_name='Анна Викторовна Соколова', email='sokolova@school.local')
    db.session.add(teacher)
    subjects = [Subject(name='Математика', color='#6c63ff'), Subject(name='Информатика', color='#14b8a6'), Subject(name='Физика', color='#f59e0b')]
    db.session.add_all(subjects)
    room = Classroom(name='204', building='Главный корпус')
    db.session.add(room)
    db.session.flush()
    admin = User(username='admin', full_name='Администратор системы', role='admin')
    admin.set_password('admin123')
    student = User(username='student', full_name='Иван Петров', role='student', class_group_id=group.id)
    student.set_password('student123')
    db.session.add_all([admin, student])
    for day, num, subject in [(1,1,subjects[0]),(1,2,subjects[1]),(2,1,subjects[2]),(3,3,subjects[0])]:
        db.session.add(Lesson(weekday=day, lesson_number=num, start_time=f'{8+num:02d}:30', end_time=f'{9+num:02d}:15', class_group_id=group.id, teacher_id=teacher.id, subject_id=subject.id, classroom_id=room.id))
    db.session.commit()
