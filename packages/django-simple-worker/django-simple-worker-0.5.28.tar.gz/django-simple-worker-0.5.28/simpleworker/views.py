from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from simpleworker.models import Task
from simpleworker.scheduler import SimpleScheduler


class WorkerStatusView(LoginRequiredMixin, TemplateView):
    template_name = 'worker_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        scheduler = SimpleScheduler()
        scheduled_jobs = scheduler.get_next_jobs()
        context['scheduled_jobs'] = scheduled_jobs

        currently_processing_query = """
        SELECT *
        FROM simpleworker_task
        WHERE id NOT IN (
            SELECT id
            FROM simpleworker_task
                FOR KEY SHARE
                    SKIP LOCKED
        )
                """
        currently_processing = list(Task.objects.raw(currently_processing_query))
        currently_processing_str = []
        currently_processing_ids = set()
        for task in currently_processing:
            currently_processing_str.append(str(task))
            currently_processing_ids.add(task.id)

        context['currently_processing'] = currently_processing_str

        next_tasks = Task.objects.all().order_by('-priority', 'id')[:30]
        context['next_tasks'] = [str(task) for task in next_tasks if task.id not in currently_processing_ids]

        return context
