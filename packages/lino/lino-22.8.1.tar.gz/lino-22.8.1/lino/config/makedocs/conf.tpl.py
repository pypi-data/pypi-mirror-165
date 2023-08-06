# -*- coding: utf-8 -*-
from pathlib import Path

{% if makedocs.language.index == 0 %}

html_context = dict(public_url="{{settings.SITE.server_url}}media/cache/help")
# from atelier.projects import add_project
# prj = add_project('..')
# prj.SETUP_INFO = dict()
# prj.config.update(use_dirhtml={{use_dirhtml}})
# prj.config.update(selectable_languages={{languages}})

# from lino.sphinxcontrib import configure

from rstgen.sphinxconf import configure ; configure(globals())
from lino.sphinxcontrib import configure ; configure(globals())

{% set interproject_specs = settings.SITE.get_plugin_setting('help', 'interproject_specs') %}
{% if interproject_specs %}
from rstgen.sphinxconf import interproject
interproject.configure(globals(), "{{interproject_specs}}")
{% endif %}


# print("20210525", prj, html_context)

project = "{{settings.SITE.title}}"
html_title = "{{settings.SITE.title}}"
{% if settings.SITE.site_config.site_company %}
import datetime
copyright = "{} {{settings.SITE.site_config.site_company}}".format(
    datetime.date.today())
{% endif %}
htmlhelp_basename = 'help'
extensions += ['lino.sphinxcontrib.logo']

{% else %}

docs = Path('../docs').resolve()
fn = docs / 'conf.py'
with open(fn, "rb") as fd:
    exec(compile(fd.read(), fn, 'exec'))

{% endif %}

language = '{{makedocs.language.django_code}}'
