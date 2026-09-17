from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models.models import ClassGroup, Teacher, Subject, Classroom

directories_bp = Blueprint('directories', __name__, url_prefix='/directories')
MAP = {'classes':(ClassGroup,'Классы','name'), 'teachers':(Teacher,'Учителя','full_name'), 'subjects':(Subject,'Предметы','name'), 'rooms':(Classroom,'Кабинеты','name')}
@directories_bp.route('/<kind>')
@login_required
def index(kind):
    if kind not in MAP: return redirect(url_for('dashboard.index'))
    model,title,field=MAP[kind]
    return render_template('directories/index.html', items=model.query.order_by(getattr(model,field)).all(), title=title, kind=kind, field=field)
@directories_bp.route('/<kind>/new', methods=['POST'])
@login_required
def create(kind):
    if not current_user.is_admin or kind not in MAP: return redirect(url_for('dashboard.index'))
    model,title,field=MAP[kind]; item=model(**{field:request.form['name']})
    db.session.add(item); db.session.commit(); flash('Запись добавлена.', 'success'); return redirect(url_for('directories.index', kind=kind))
