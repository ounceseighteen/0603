from flask import Blueprint, send_file
from flask_login import login_required, current_user
from pathlib import Path

backup_bp = Blueprint('backup', __name__, url_prefix='/backup')
@backup_bp.route('/')
@login_required
def download():
    if not current_user.is_admin: return 'Forbidden', 403
    db_path = Path(__file__).resolve().parents[2] / 'instance' / 'schedule.db'
    return send_file(db_path, as_attachment=True, download_name='school_schedule_backup.db')
