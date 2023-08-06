import importlib
import logging
import os
import pkgutil
import signal
import sys
from typing import List
from typing import Type

from apscheduler.events import EVENT_ALL
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.apps import apps
from django.utils.module_loading import module_has_submodule

from simpleworker.simple_task import SimpleTask

logger = logging.getLogger(__name__)


class SimpleScheduler:
    def __init__(self):
        self.import_tasks_modules()

    def _is_package(self, module):
        module_path = getattr(module, "__path__", None)
        return module_path and os.path.isdir(module_path[0])

    def _get_submodules(self, package):
        submodules = []

        package_path = package.__path__
        prefix = package.__name__ + "."

        for _, module_name, is_pkg in pkgutil.walk_packages(package_path, prefix):
            if is_pkg:
                sub_submodules = self._get_submodules(importlib.import_module(module_name))
                submodules.extend(sub_submodules)
            else:
                submodules.append(module_name)

        return submodules

    def _resolve_executable(self, exec_name):
        bin_dir = os.path.dirname(sys.executable)
        if bin_dir:
            return os.path.join(bin_dir, exec_name)
        return exec_name

    def import_tasks_modules(self):
        app_configs = (c for c in apps.get_app_configs() if module_has_submodule(c.module, "tasks"))

        for conf in app_configs:
            module = conf.name + ".tasks"

            imported_module = importlib.import_module(module)
            if not self._is_package(imported_module):
                logger.info("Imported tasks module: %r" % module)
            else:
                submodules = self._get_submodules(imported_module)
                for submodule in submodules:
                    logger.info("Imported tasks module: %r" % submodule)

    def _get_scheduler(self, scheduler_type=BlockingScheduler):
        scheduler = scheduler_type(
            {
                'apscheduler.executors.default': {
                    'class': 'apscheduler.executors.debug:DebugExecutor',
                },
            }
        )

        cls: Type[SimpleTask]
        for cls in SimpleTask.__subclasses__():
            if cls.cron is not None:
                logger.info(f'Task {cls.__name__} scheduled on {cls.cron}')
                trigger = CronTrigger.from_crontab(cls.cron)
                scheduler.add_job(cls().send, trigger=trigger, name=cls.__name__)

        return scheduler

    def get_background_scheduler(self):
        scheduler = self._get_scheduler(BackgroundScheduler)
        return scheduler

    def get_next_jobs(self) -> List:
        scheduler = self.get_background_scheduler()
        scheduler.start(paused=True)

        jobs = sorted(scheduler.get_jobs(), key=lambda x: (x.next_run_time, x.name))
        run_times = [f'{job.name} at {job.next_run_time}' for job in jobs]

        scheduler.shutdown(wait=False)
        del scheduler

        return run_times

    def run(self):
        logger.info("Starting scheduler")

        scheduler = self._get_scheduler()

        def shutdown(signum, frame):
            logger.info('Shutting down scheduler')
            scheduler.shutdown()

        def exit_listener(event):
            if hasattr(event, 'exception') and event.exception is not None:
                scheduler.shutdown()
                logger.exception(event.exception)
                try:
                    from sentry_sdk import capture_exception
                    capture_exception(event.exception)
                except Exception as e:
                    logger.exception(e)

        scheduler.add_listener(exit_listener, EVENT_ALL)

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        scheduler.start()
