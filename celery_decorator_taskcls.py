"""
This package is temporary way to get `app.taskcls` decorator right now.
The main target of this package make you able to use taskcls decorator
before celery 4.5 released, and then you can remove this package import
*without* application code change
More about: https://github.com/celery/celery/pull/5755
"""

from functools import wraps


def taskcls(self, *args, **opts):
    """Class decarator to create a task class from
    any class with fabric classmethod `task`.

    Example:
        .. code-block:: python

            class BaseTask:
                "We can define common behavior here"

                def __init__(self, *args, **kwargs):
                    "Any behavior"

                @classmethod
                def task(cls, *args, **kwargs):
                    instance = cls(*args, **kwargs)
                    return instance.main()

            @app.taskcls
            class SimpleTask(BaseTask):
                def main(self):
                    ...

            @app.taskcls(bind=True, name='custom_name')
            class AnotherTask(BaseTask):
                "You can pass here the same args as app.task"
                def main(self):
                    ...

    And sending task almost the same:
        .. code-block:: python

            SimpleTask.task.delay(...)

    OR by name
        .. code-block:: python

            # Default
            task = app.tasks['my_module.SimpleTask']
            task.delay(...)

            # Custom
            task = app.tasks['custom_name']
            task.delay(...)

    Default task options can be passed by inner class `MetaTask`:
        .. code-block:: python

            class BaseTask:
                class MetaTask:
                    bind = True

                @classmethod
                def task(cls, *args, **kwargs):
                    ...
    """

    def inner_taskcls(cls):
        # Workaround: task name can not be generated automatically
        if 'name' not in opts:
            opts['name'] = self.gen_task_name(
                cls.__name__,
                cls.__module__,
            )

        # Feature: allow to inherit taskcls from another taskcls
        original_cls_task = cls.task
        original_cls_task_class = original_cls_task.__class__
        
        if issubclass(original_cls_task_class, self.Task):
            original_cls_task = cls.__task__
        else:
            cls.__task__ = classmethod(original_cls_task.__func__)

        # Feature: nested MetaTask class support
        if hasattr(cls, 'MetaTask'):
            meta_instance = cls.MetaTask()
            task_opts = {
                key: getattr(meta_instance, key)
                for key in dir(meta_instance)
                if not key.startswith('__')
            }
            task_opts.update(opts)
        else:
            task_opts = opts

        # Core taskcls implementation
        @self.task(**task_opts)
        @wraps(original_cls_task)
        def taskcls_task(*task_args, **task_kwargs):
            return original_cls_task(*task_args, **task_kwargs)

        cls.task = taskcls_task
        return cls

    # Feature: allow to use taskcls decorator without kwargs
    if len(args) == 0:
        return inner_taskcls

    if len(args) != 1:
        raise ValueError

    return inner_taskcls(args[0])


def patch_celery(force=False):
    from celery.app.base import Celery

    if hasattr(Celery, 'taskcls') and not force:
        return

    Celery.taskcls = taskcls
