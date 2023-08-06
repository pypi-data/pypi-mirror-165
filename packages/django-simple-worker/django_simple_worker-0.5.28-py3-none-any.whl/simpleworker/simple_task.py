from distutils.util import strtobool
from typing import Optional

from django.conf import settings


class SimpleTask:
    queue: str = 'default'
    max_retries: Optional[int] = None
    cron: Optional[str] = None

    # Tasks with higher priority are executed first
    priority: int = 100

    # Exclusive task allow execution of only one task with the same name at a time
    exclusive: bool = False

    def get_name(self) -> str:
        return self.__class__.__name__

    def _send(self, seconds_delay: Optional[int] = None):
        if hasattr(settings, 'SIMPLE_WORKER_SYNC_PROCESSING') and strtobool(str(settings.SIMPLE_WORKER_SYNC_PROCESSING)):
            self.handle()
        else:
            from simpleworker.models import Task
            return Task.add(self, seconds_delay)

    def send(self):
        return self._send()

    def send_delayed(self, seconds_delay: int):
        return self._send(seconds_delay)

    def handle(self):
        raise NotImplementedError('Handle method must be implemented')
