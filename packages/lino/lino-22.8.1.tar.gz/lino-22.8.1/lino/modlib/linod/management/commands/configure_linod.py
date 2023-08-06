# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from importlib.util import find_spec
# has_channels = find_spec('channels') is not None
# if not has_channels:
#     raise Exception("No django-channels installed!")

import os
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand

from getlino.utils import Installer
from jinja2 import Template

from lino.modlib.linod.utils import LINOD

SUPERVISOR_CONF_PREFIX = "linod_"
SUPERVISOR_CONF_DIR = "/etc/supervisor/conf.d/"

class Command(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'channels', nargs='*', help="The names of the channels to run!")
        parser.add_argument(
            '--output-dir', '-o', dest='output_dir',
            help="The directory at which to put the rendered supervisor conf!")

    def handle(self, *args, **options):
        output_dir = Path(options.get('output_dir', None) or SUPERVISOR_CONF_DIR)
        channels = options.get('channels', [])
        if LINOD not in channels:
            channels.append(LINOD)
        project_name=settings.SITE.project_name
        context = dict(
            project_name=project_name,
            settings_module=str(os.environ['DJANGO_SETTINGS_MODULE']),
            env_activate=str(Path(os.environ['_']).parent / 'activate'),
            project_path=str(settings.SITE.project_dir),
            channels=' '.join(channels)
        )
        cmd_dir = Path(__file__).parent
        template = cmd_dir / 'etc' / 'runworker_supervisor_conf_template.txt'
        with open(template) as f:
            t = Template(f.read())
        conf = t.render(context)
        filename = (SUPERVISOR_CONF_PREFIX + project_name + ".conf")
        temp_file = cmd_dir / 'temp'/ filename
        output_file = output_dir / filename
        with open(temp_file, "w") as f:
            f.write(conf)
        i = Installer()
        i.runcmd_sudo(f"mv {temp_file} {output_file}")

class CleanUp(BaseCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--supervisor-dir', '-d', dest='supervisor_dir', default=SUPERVISOR_CONF_DIR,
            help="The directory from which to clear the rendered supervisor conf!")

    def handle(self, *args, **options):
        clearables = Path(options.get('supervisor_dir')) / (SUPERVISOR_CONF_PREFIX + "*")
        i = Installer()
        i.runcmd_sudo(f"rm {clearables}")
