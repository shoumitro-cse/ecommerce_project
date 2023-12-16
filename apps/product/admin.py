from django.apps import apps
from django.contrib import admin

app_models = apps.get_app_config('product').get_models()
admin.site.register(list(app_models))
