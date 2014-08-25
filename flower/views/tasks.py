from __future__ import absolute_import

import celery

from tornado import web

from ..views import BaseHandler
from ..models import TaskModel, WorkersModel


class TaskView(BaseHandler):
    @web.authenticated
    def get(self, task_id):
        task = TaskModel.get_task_by_id(self.application, task_id)
        if task is None:
            raise web.HTTPError(404, "Unknown task '%s'" % task_id)

        self.render("task.html", task=task)


class TasksView(BaseHandler):
    @web.authenticated
    def get(self):
        app = self.application
        limit = self.get_argument('limit', default=None, type=int)
        worker = self.get_argument('worker', None)
        type = self.get_argument('type', None)
        state = self.get_argument('state', None)

        worker = worker if worker != 'All' else None
        type = type if type != 'All' else None
        state = state if state != 'All' else None

        tasks = TaskModel.iter_tasks(app, limit=limit, type=type,
                                     worker=worker, state=state)
        workers = WorkersModel.get_workers(app)
        seen_task_types = TaskModel.seen_task_types(app)

        self.render("tasks.html", tasks=tasks,
                    task_types=seen_task_types,
                    all_states=celery.states.ALL_STATES,
                    workers=workers,
                    limit=limit,
                    worker=worker,
                    type=type,
                    state=state)


class TasksMatchView(BaseHandler):
    @web.authenticated
    def get(self):
        app = self.application
        limit = self.get_argument('limit', default=None, type=int)
        worker = self.get_argument('worker', None)
        pattern = self.get_argument('pattern', None)
        state = self.get_argument('state', None)

        worker = worker if worker != 'All' else None
        pattern = pattern if type != '.*' else None
        state = state if state != 'All' else None

        tasks = TaskModel.iter_tasks_with_pattern(app, limit=limit, pattern=pattern,
                                     worker=worker, state=state)
        workers = WorkersModel.get_workers(app)
        seen_task_types = TaskModel.seen_task_types(app)

        self.render("tasks.html", tasks=tasks,
                    task_types=seen_task_types,
                    all_states=celery.states.ALL_STATES,
                    workers=workers,
                    limit=limit,
                    worker=worker,
                    type=type,
                    state=state)
