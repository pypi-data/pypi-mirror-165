# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from lino.modlib.linod.utils import LINOD

class Command(BaseCommand):
    def handle(self, *args, **options):
        async_to_sync(get_channel_layer().send)(LINOD, {'type': 'initiate'})
