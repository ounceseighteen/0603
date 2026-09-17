from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models.models import Lesson, ClassGroup, Teacher, Subject, Classroom

dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/')
@login_required
def index():
    lessons = Lesson.query.filter_by(class_group_id=current_user.class_group_id).order_by(Lesson.weekday, Lesson.lesson_number).all() if current_user.class_group_id else Lesson.query.order_by(Lesson.weekday, Lesson.lesson_number).all()
    return render_template('dashboard/index.html', lessons=lessons, counts={'lessons':Lesson.query.count(),'classes':ClassGroup.query.count(),'teachers':Teacher.query.count(),'subjects':Subject.query.count(),'rooms':Classroom.query.count()})
