import os

def clear_celery_backend_files():
    print("clear")
    try:
        for f in ["celery.sqlite", "celerybeat-schedule"]:
            print(f, os.path.exists(f))
            if os.path.exists(f):
                os.remove(f)
    except Exception as e:
        print("Problem while removing Celery backend sqlite files", str(e))

