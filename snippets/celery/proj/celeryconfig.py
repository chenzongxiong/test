BROKER_URL = 'amqp://admin:admin@10.18.10.75:5673//'
CELERY_RESULT_BACKEND = 'redis://localhost'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

# CELERY_ROUTES = {
#     'tasks.add': 'low-priority',
# }
CELERY_ANNOTATIONS = {
    '*': {'rate_limit': '10/m'}
}
CELERY_IMPORTS = ('proj.tasks',)
