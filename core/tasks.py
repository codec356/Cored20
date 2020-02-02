from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from Cored20.celery import app

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/1')), name="task_update_auction", ignore_result=True)
def task_update_auction(*args, **opts):
    print('lalaal task execution')
    logger.info("Updated repo was requested with params:\nopts={}\nargs={}".format(opts, args))
