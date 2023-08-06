# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from importlib.util import find_spec
has_channels = find_spec('channels') is not None
if has_channels:
    from channels.management.commands.runworker import Command
else:
    raise Exception("No django-channels installed!")
