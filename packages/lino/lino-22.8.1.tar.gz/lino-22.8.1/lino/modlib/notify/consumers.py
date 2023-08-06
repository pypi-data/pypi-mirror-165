# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from channels.generic.websocket import AsyncWebsocketConsumer
class ClientConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(self.scope['user'].username, self.channel_name)

    async def send_notification(self, text):
        await self.send(text_data=text['text'])

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.scope['user'].username, self.channel_name)
