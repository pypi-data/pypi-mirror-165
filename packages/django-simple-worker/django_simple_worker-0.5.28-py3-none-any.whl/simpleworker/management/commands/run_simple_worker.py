import logging
import os
import signal
from multiprocessing import Process
from time import sleep
from typing import List, Dict

import django
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def setup_django(env: Dict):
    for key, value in env.items():
        if os.getenv(key) is None:
            os.environ[key] = value
    django.setup()


def run_scheduler(env: Dict):
    setup_django(env)

    from simpleworker.scheduler import SimpleScheduler

    scheduler = SimpleScheduler()
    scheduler.run()


def run_worker(queues: List[str], max_processed_tasks: int, env: Dict):
    setup_django(env)
    from simpleworker.simple_worker import SimpleWorker

    worker = SimpleWorker(queues, max_processed_tasks)
    worker.run()


class Command(BaseCommand):
    should_exit: bool = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--queue',
            action='append',
            default=[],
            dest='queues',
        )
        parser.add_argument(
            '--with_cron',
            action='store_true',
            default=False,
            dest='with_cron',
        )
        parser.add_argument(
            '--max_processed_tasks',
            action='store',
            default=0,
            dest='max_processed_tasks',
        )

    def run_with_cron(self, queues: List[str], max_processed_tasks: int):
        env = dict(os.environ)

        scheduler_process = Process(target=run_scheduler, kwargs={'env': env})
        scheduler_process.daemon = True
        scheduler_process.start()

        worker_process = Process(target=run_worker, args=(queues, max_processed_tasks), kwargs={'env': env})
        worker_process.daemon = True
        worker_process.start()

        processes: List[Process] = [
            worker_process,
            scheduler_process,
        ]

        def shutdown(signum, frame):
            logger.info(f'Exit requested signal={signum}')
            self.should_exit = True

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        while not self.should_exit:
            for process in processes:
                if not process.is_alive():
                    self.should_exit = True
                sleep(1)
        for process in processes:
            process.join(timeout=1)
        logger.info('Worker process exiting')

    def handle(self, *args, **options):
        queues: List[str] = options['queues']
        with_cron = options['with_cron']
        max_processed_tasks = options['max_processed_tasks']

        if with_cron:
            self.run_with_cron(queues, max_processed_tasks)
        else:
            run_worker(queues, max_processed_tasks, {})
