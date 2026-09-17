from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models.models import Lesson, ClassGroup, Teacher, Subject, Classroom
from ..services.conflict_checker import find_conflict

schedule_bp = Blueprint('schedule', __name__, url_prefix='/schedule')
DAYS = {1:'Понедельник',2:'Вторник',3:'Среда',4:'Четверг',5:'Пятница',6:'Суббота'}
@schedule_bp.route('/')
@login_required
def index():
    day = request.args.get('day', type=int)
    query = Lesson.query
    if day: query = query.filter_by(weekday=day)
    lessons = query.order_by(Lesson.weekday, Lesson.lesson_number).all()
    return render_template('schedule/index.html', lessons=lessons, days=DAYS, selected_day=day)
@schedule_bp.route('/new', methods=['GET','POST'])
@login_required
def create():
    if not current_user.is_admin: flash('Недостаточно прав.', 'error'); return redirect(url_for('schedule.index'))
    if request.method == 'POST':
        data = {k:int(request.form[k]) for k in ['weekday','lesson_number','class_group_id','teacher_id','subject_id','classroom_id']}
        data.update(start_time=request.form['start_time'], end_time=request.form['end_time'])
        error = find_conflict(data)
        if error: flash(error, 'error')
        else: db.session.add(Lesson(**data)); db.session.commit(); flash('Занятие добавлено.', 'success'); return redirect(url_for('schedule.index'))
    return render_template('schedule/form.html', lesson=None, days=DAYS, classes=ClassGroup.query.all(), teachers=Teacher.query.all(), subjects=Subject.query.all(), rooms=Classroom.query.all())
@schedule_bp.route('/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete(lesson_id):
    if current_user.is_admin:
        lesson = db.session.get(Lesson, lesson_id)
        if lesson: db.session.delete(lesson); db.session.commit(); flash('Занятие удалено.', 'success')
    return redirect(url_for('schedule.index'))
