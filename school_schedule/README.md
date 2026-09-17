# SchoolFlow — АИС «Расписание школы»

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate      # macOS/Linux
pip install -r requirements.txt
python run.py
```

Откройте http://127.0.0.1:5000

## Демо-доступ

- Администратор: `admin` / `admin123`
- Ученик: `student` / `student123`

При первом запуске автоматически создаётся SQLite-база в `instance/schedule.db` и добавляются демонстрационные данные.
