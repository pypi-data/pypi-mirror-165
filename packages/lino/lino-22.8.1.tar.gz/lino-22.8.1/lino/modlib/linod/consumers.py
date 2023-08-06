# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
import json
import pickle
import asyncio
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from lino.api import rt, dd

try:
    from pywebpush import webpush, WebPushException
except ImportError:
    webpush = None

from channels.consumer import AsyncConsumer

import logging
import socketserver
import struct

logger = logging.getLogger('linod')

class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    def handle(self):
        chunk = self.connection.recv(4)
        if len(chunk) < 4:
            return
        slen = struct.unpack('>L', chunk)[0]
        chunk = self.connection.recv(slen)
        while len(chunk) < slen:
            chunk = chunk + self.connection.recv(slen - len(chunk))
        obj = self.unPickle(chunk)
        record = logging.makeLogRecord(obj)
        self.handleLogRecord(record)

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        logger.handle(record)

class LogRecordSocketReceiver(socketserver.ThreadingUnixStreamServer):
    allow_reuse_address = True

    def __init__(self, host, handler=LogRecordStreamHandler):
        super().__init__(host, handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

class LinodConsumer(AsyncConsumer):

    async def log_server(self):
        log_sock = str(Path(settings.SITE.project_dir) / 'log_sock')
        try:
            os.unlink(log_sock)
        except OSError:
            pass
        with LogRecordSocketReceiver(log_sock) as server:
            try:
                server.serve_forever()
            finally:
                server.server_close()
                server.shutdown()

    async def send_push(self, event):
        # logger.info("Push to %s : %s", user or "everyone", data)
        data = event['data']
        user = event['user_id']
        if user is not None:
            user = rt.models.users.User.objects.get(pk=user)
        kwargs = dict(
            data=json.dumps(data),
            vapid_private_key=dd.plugins.notify.vapid_private_key,
            vapid_claims={
                'sub': "mailto:{}".format(dd.plugins.notify.vapid_admin_email)
            }
        )
        if user is None:
            subs = rt.models.notify.Subscription.objects.all()
        else:
            subs = rt.models.notify.Subscription.objects.filter(user=user)
        for sub in subs:
            sub_info = {
                'endpoint': sub.endpoint,
                'keys': {
                    'p256dh': sub.p256dh,
                    'auth': sub.auth,
                },
            }
            try:
                req = webpush(subscription_info=sub_info, **kwargs)
            except WebPushException as e:
                if e.response.status_code == 410:
                    sub.delete()
                else:
                    raise e

    async def repeat_schedule(self, initial_td, td, coro):
        await asyncio.sleep(initial_td)
        asyncio.ensure_future(self.repeat_schedule(td, td, coro))
        asyncio.ensure_future(coro())

    async def initiate(self, event):
        asyncio.ensure_future(self.log_server())
        asyncio.ensure_future(self.run_schedule())

    async def run_schedule(self):
        for at, td, coro in dd.SCHEDULES:
            now = timezone.now()
            if at is not None:
                when = now.replace(hour=at.tm_hour, minute=at.tm_min, second=0, microsecond=0)
                if now.hour > at.tm_hour or (now.hour == at.tm_hour and now.minute >= at.tm_min):
                    when = when + timezone.timedelta(days=1)
                initial_td = int((when - now).total_seconds())
                td = int(timezone.timedelta(hours=24).total_seconds())
            else:
                when = timezone.now()
                initial_td = 0
                td = int(td.total_seconds())
            asyncio.ensure_future(self.repeat_schedule(initial_td, td, coro))
