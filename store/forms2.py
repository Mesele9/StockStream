# forms.py
from django import forms
from .models import Item, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description', 'category', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock']

class PurchaseRecordForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecord
        fields = ['date', 'supplier', 'purchaser', 'upload_receipt']

class PurchaseRecordItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecordItem
        fields = ['item', 'quantity', 'unit_price', 'total_price']

class IssueRecordForm(forms.ModelForm):
    class Meta:
        model = IssueRecord
        fields = ['date', 'department', 'issued_by', 'received_by']

class IssueRecordItemForm(forms.ModelForm):
    class Meta:
        model = IssueRecordItem
        fields = ['item', 'quantity', 'unit_price', 'total_price']

