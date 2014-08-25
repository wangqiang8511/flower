from __future__ import absolute_import

from tornado import web
from tornado.options import define, options
from celery.app.utils import find_app

from ..views import BaseHandler
from ..models import SchedulesModel
from ..utils.beat_inspect import inspect_all_beats


class SchedulesView(BaseHandler):
    @web.authenticated
    def get(self):
        app_file = options.app_file
        registered_apps = []
        with open(app_file, 'r') as f:
            for line in f:
                registered_apps.append(line.strip())
        schedules = inspect_all_beats(registered_apps)
        all_schedules = {}
        for schedule in schedules:
            celery_app = schedule['task'].split(".")[0]
            all_schedules[celery_app] = all_schedules.get(celery_app, []) + [schedule]

        self.render("schedules.html", schedules=all_schedules)
