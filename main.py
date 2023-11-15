# main.py

from celery.schedules import crontab

from tasks import *

# Set the Celery beat schedule and timezone
celery.conf.beat_schedule = {
    'send-styled-email-every-evening': {
        'task': 'tasks.send_email',
        'schedule': crontab(hour=17, minute=30),
        'args': (sender_email, sender_password, subject, html_body),
    },
}
celery.conf.timezone = 'Asia/Kolkata'

# celery -A main beat --logl evel=info
# └─$ celery -A tasks worker --loglevel=info
celery.conf.beat_schedule = {
    'send-monthly-report-every-month': {
        'task': 'tasks.send_report',
        'schedule': crontab(hour=15, minute=33, day_of_month=1),
        'args': None,
    },
}
celery.conf.timezone = 'Asia/Kolkata'


celery.conf.beat_schedule = {
    'dynamic-pricing-every-6-hours': {
        'task': 'tasks.dynamic_pricing',
        'schedule': crontab(minute=0, hour='*/6'),
        'args': None,
    },
}
celery.conf.timezone = 'Asia/Kolkata'
