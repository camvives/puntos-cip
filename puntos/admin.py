from django.contrib import admin
from .models import Entrada, Seccion, TipoOracion

# Register your models here.
admin.site.register(Seccion)
admin.site.register(TipoOracion)
admin.site.register(Entrada)