import xadmin
from xadmin import views

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSettings(object):
    site_title = "Hippo后台"
    site_footer = '牛逼的后台'
    menu_style = 'accordion'

xadmin.site.register(views.CommAdminView, GlobalSettings)