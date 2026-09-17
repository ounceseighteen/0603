from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models.models import User

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'].strip()).first()
        if user and user.check_password(request.form['password']):
            login_user(user); return redirect(url_for('dashboard.index'))
        flash('Неверный логин или пароль.', 'error')
    return render_template('auth/login.html')
@auth_bp.route('/logout')
@login_required
def logout(): logout_user(); return redirect(url_for('auth.login'))
