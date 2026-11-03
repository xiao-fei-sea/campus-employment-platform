from app.celery_app import celery_app


@celery_app.task
def daily_backup():
    return {"status": "success", "message": "Daily backup task placeholder"}


@celery_app.task
def export_employment_data(start_date: str, end_date: str):
    return {"status": "success", "message": "Export employment data task placeholder"}


@celery_app.task
def export_student_list(major: str = None, graduation_year: int = None):
    return {"status": "success", "message": "Export student list task placeholder"}
