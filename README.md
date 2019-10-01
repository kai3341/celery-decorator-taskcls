Celery Decorator taskcls
===============

* Free software: MIT License

This package is temporary way to get `app.taskcls` decorator right now.
The main target of this package make you able to use taskcls decorator
before celery 4.5 released, and then you can remove this package import
*without* application code change

More about: https://github.com/celery/celery/pull/5755

Features
--------


```
import celery_decorator_taskcls
celery_decorator_taskcls.patch_celery()

from celery import Celery
app = Celery(...)

class BaseTask:
    def __init__(self, task, **kwargs):
        self.task = task
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def task(cls, task, **kwargs):
        instance = cls(task, **kwargs)
        return instance.main()


@app.taskcls(bind=True)
class SimpleTask(BaseTask):
    def main(self):
        ...
```

`app.taskcls` decorator behavior is the same as `app.task`. You can pass it
kwargs like `bind`, `name` or other or you can use it without kwargs

You can also pass default decorator options by nested class `MetaTask`:

```
class BaseTask:
    class MetaTask:
        bind = True

    @classmethod
    def task(cls, taks, *args, **kwargs):
        ...
```

Patching options
--------
By default patcher search `Celery.taskcls` attribute. If it not found, patcher
creates it. But when it exists (I belive you find it in Celery 4.5), patcher
checks its optional argument `force`, because it seems patching not required.
Calling `celery_decorator_taskcls.patch_celery(force=True)` enforces
patching Celery even `Celery.taskcls` exists
