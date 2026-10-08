from django.contrib import admin

from .models import Herramienta

@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "marca")
    search_fields = ("nombre", "marca")
    list_filter = ("categoria", "marca")
