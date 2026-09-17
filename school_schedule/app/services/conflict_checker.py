from ..models.models import Lesson

def find_conflict(data, current_id=None):
    query = Lesson.query.filter_by(weekday=data['weekday'], lesson_number=data['lesson_number'])
    if current_id: query = query.filter(Lesson.id != current_id)
    for lesson in query.all():
        if lesson.teacher_id == data['teacher_id']: return 'Этот учитель уже ведёт занятие в выбранное время.'
        if lesson.class_group_id == data['class_group_id']: return 'У этого класса уже есть занятие в выбранное время.'
        if lesson.classroom_id == data['classroom_id']: return 'Этот кабинет уже занят в выбранное время.'
    return None
