# celeryconfig.py
# (for RabbitMQ)
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks", )
