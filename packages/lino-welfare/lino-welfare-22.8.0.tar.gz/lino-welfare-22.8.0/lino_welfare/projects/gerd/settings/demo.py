import datetime

from lino_welfare.projects.gerd.settings import *

class Site(Site):
    languages = 'de fr en'
    is_demo_site = True
    the_demo_date = datetime.date(2014, 5, 22)
    # ignore_dates_after = datetime.date(2019, 05, 22)
    use_java = False
    webdav_protocol = 'webdav'
    # default_ui = "lino_react.react"

    #beid_protocol = 'beid'
    # migrations_package = "lino_welfare.projects.gerd.migrations"

    def get_plugin_configs(self):
        yield super(Site, self).get_plugin_configs()
        yield ('extjs', 'autorefresh_seconds', 5)

    # def get_default_language(self):
    #     return 'de'


SITE = Site(globals())
# SITE.appy_params.update(raiseOnError=False)
# SITE.plugins.extjs.configure(autorefresh_seconds=5)

DEBUG = True
