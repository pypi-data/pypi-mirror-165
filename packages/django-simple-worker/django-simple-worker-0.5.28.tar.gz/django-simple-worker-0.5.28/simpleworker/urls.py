from django.urls import path

from simpleworker.views import WorkerStatusView

urlpatterns = [
    path('', WorkerStatusView.as_view(), name='simpleworker'),
]
