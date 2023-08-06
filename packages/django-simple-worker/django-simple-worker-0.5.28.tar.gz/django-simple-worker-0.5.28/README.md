
# Django Simple Worker


#### Installation
```shell
pip install django-simple-worker
```

Add to installed apps:
```python
INSTALLED_APPS = [
    'simpleworker',
]
```

Add to your urls (optional):
```python
path('simpleworker/', include(('simpleworker.urls', 'simpleworker'), namespace='simpleworker')),
```

#### Configuration
Add to Django settings:
```python
SIMPLE_WORKER_SYNC_PROCESSING = env.bool('SIMPLE_WORKER_SYNC_PROCESSING', default=False)
```

#### Usage
TODO
