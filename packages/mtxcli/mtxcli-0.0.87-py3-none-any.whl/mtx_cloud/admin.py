from django.apps import apps
from django.contrib import admin
from .models import SshHost

# class SshHostAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(SshHost, SshHostAdmin)




# 自动注册（会将所有app的model都自动注册进来）
class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass