from app.db import db, Task


def create_task(user, type):
    try:
        # Проверяем существование задачи для пользователя
        existing_task = Task.query.filter_by(user_id=user).first()

        if existing_task:
            # Если статус 'pending', ничего не делаем
            if existing_task.status == 'pending':
                return {"success": False, "error": "Task already exists with status 'pending'."}

            # Если статус другой, обновляем его на 'pending'
            existing_task.status = 'pending'
            db.session.commit()
            return {"success": True, "message": "Task status updated to 'pending'."}

        # Если задачи нет, создаем новую
        task = Task(
            user_id=user,
            tasktype=type,
            status='pending',
        )
        db.session.add(task)
        db.session.commit()
        return {"success": True, "message": "New task created."}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}
