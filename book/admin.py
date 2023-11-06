from django.contrib import admin

# Register your models here.

from .models import Ledger, Entry

admin.site.register(Ledger)
admin.site.register(Entry)
