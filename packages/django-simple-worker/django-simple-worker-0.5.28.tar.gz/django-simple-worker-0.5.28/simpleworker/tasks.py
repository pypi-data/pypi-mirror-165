import logging
from datetime import timedelta

from django.utils import timezone

from simpleworker.models import TaskResult
from simpleworker.simple_task import SimpleTask

logger = logging.getLogger(__name__)


class TaskResultCleanup(SimpleTask):
    cron = '0 0 * * *'

    def handle(self):
        logger.info("Cleaning up task results")
        TaskResult.objects.filter(finished__lte=timezone.now() - timedelta(days=7)).delete()
        logger.info("Cleaning up task results finished")
