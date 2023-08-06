# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from importlib.util import find_spec
has_channels = find_spec('channels') is not None
import logging

class LinodFilter(logging.Filter):
    def filter(self, record):
        return 1

if has_channels:
    from django.conf import settings

    class LinodFilter(logging.Filter):
        def filter(self, record):
            if record.name.split('.')[0] in settings.SITE.auto_configure_logger_names:
                return 0
            return 1
