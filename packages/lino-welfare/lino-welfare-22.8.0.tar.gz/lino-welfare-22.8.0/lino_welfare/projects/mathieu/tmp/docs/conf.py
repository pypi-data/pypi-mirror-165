# -*- coding: utf-8 -*-
from pathlib import Path



html_context = dict(public_url="http://127.0.0.1:8000/media/cache/help")
# from atelier.projects import add_project
# prj = add_project('..')
# prj.SETUP_INFO = dict()
# prj.config.update(use_dirhtml=False)
# prj.config.update(selectable_languages=['fr', 'nl', 'de', 'en'])

# from lino.sphinxcontrib import configure

from rstgen.sphinxconf import configure ; configure(globals())
from lino.sphinxcontrib import configure ; configure(globals())


# lino_welfare

from rstgen.sphinxconf import interproject
interproject.configure(globals(), "lino_welfare")



# print("20210525", prj, html_context)

project = "mathieu"
html_title = "mathieu"

import datetime
copyright = "{} ÖSHZ Kettenis".format(
    datetime.date.today())

htmlhelp_basename = 'help'
extensions += ['lino.sphinxcontrib.logo']



language = 'fr'