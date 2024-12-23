from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time

is_task_running = False


def long_task():
    print("running")

    global is_task_running
    if is_task_running:
        print("Задача уже выполняется, пропуск...")
        return

    is_task_running = True
    print("Задача началась...")
    time.sleep(60)  # Имитация долгой задачи
    is_task_running = False
    print("Задача завершена.")


def check_and_run_tasks():
    print("Check and run tasks...")

    # Проверка и выполнение задач
    long_task()


def start_scheduler():
    print("Instalization")
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_and_run_tasks,
        IntervalTrigger(minutes=1),
        id='task_checker',
        name='Проверка и выполнение задач',
        replace_existing=True
    )
    scheduler.start()



