from __future__ import absolute_import
from celery import Celery


app = Celery('proj')
             # broker='amqp://admin:admin@10.18.10.75:5673//',
             # backend='redis://localhost',
             # include=['proj.tasks'])

# app.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
#     )
app.config_from_object('proj.celeryconfig')

if __name__ == '__main__':
    app.start()
