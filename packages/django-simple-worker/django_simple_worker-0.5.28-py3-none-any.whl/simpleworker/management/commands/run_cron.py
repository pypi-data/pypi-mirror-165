import logging

from django.core.management.base import BaseCommand

from simpleworker.scheduler import SimpleScheduler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Start the task scheduler"

    def handle(self, *args, **options):
        scheduler = SimpleScheduler()
        scheduler.run()
