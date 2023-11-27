from django.contrib import admin

from .models import Ledger, Entry

class LedgerAdmin(admin.ModelAdmin):
    # list_display = ('id', 'title', 'icon', 'date_created', 'description')
    list_display = ('id', 'title', 'icon', 'date_created', 'description', 'display_entries_id')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_per_page = 25
    
    readonly_fields = ('display_id', 'display_entries') # 不能直接通过fields指定display_id
    # 显示账本ID
    def display_id(self, obj):
        return obj.pk
    display_id.short_description = 'ID'
    # 显示账本下的所有明细，仅ID
    def display_entries_id(self, obj):
        return ", ".join([str(entry.pk) for entry in obj.entries.all()])
    display_entries_id.short_description = 'Entries ID'
    # 显示账本下的所有明细，包括ID和标题
    def display_entries(self, obj):
        return "\n".join([f"{entry.id}, {entry.title}" for entry in obj.entries.all()])
    display_entries.short_description = 'Entries'

    

class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'entry_type', 'amount', 'category', 'date_created', 'notes')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'notes')
    list_per_page = 25


admin.site.register(Ledger, LedgerAdmin)
admin.site.register(Entry, EntryAdmin)
