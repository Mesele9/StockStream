
from django.contrib import admin
from .models import Item, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem

class PurchaseRecordItemInline(admin.TabularInline):
    model = PurchaseRecordItem
    extra = 1

class PurchaseRecordAdmin(admin.ModelAdmin):
    inlines = [PurchaseRecordItemInline]

admin.site.register(Item)
admin.site.register(PurchaseRecord, PurchaseRecordAdmin)
admin.site.register(IssueRecord)

