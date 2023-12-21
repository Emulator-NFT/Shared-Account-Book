from django.contrib import admin

from .models import Ledger, LedgerMember, Entry, EntryImage, Category, Budget

class LedgerMemberInline(admin.TabularInline):
    model = LedgerMember
    extra = 1

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    readonly_fields = ('display_id',)

    def display_id(self, obj):
        return obj.pk
    display_id.short_description = 'ID'

class LedgerAdmin(admin.ModelAdmin):
    # list_display = ('id', 'title', 'icon', 'date_created', 'description')
    list_display = ('id', 'title', 'icon', 'date_created', 'description', 'display_entries_id')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_per_page = 25
    
    readonly_fields = ('display_id', 'display_entries') # 不能直接通过fields指定display_id
    inlines = [LedgerMemberInline, CategoryInline] # 在Ledger的管理页面上，直接添加、编辑或删除与该Ledger关联的LedgerMember对象
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


class EntryImageInline(admin.TabularInline):
    model = EntryImage
    extra = 1

class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'entry_type', 'amount', 'category', 'date_created', 'notes')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'notes')
    list_per_page = 25
    inlines = [EntryImageInline] # 在Entry的管理页面上，直接添加、编辑或删除与该Entry关联的EntryImage对象。

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'ledger', 'name', 'icon', 'category_type')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)
#     list_per_page = 25

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'ledger', 'total', 'year', 'quarter', 'month', 'week', 'day')
    list_display_links = ('id', 'ledger')
    search_fields = ('ledger',)
    list_per_page = 25

admin.site.register(Ledger, LedgerAdmin)
admin.site.register(Entry, EntryAdmin)
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Budget, BudgetAdmin)