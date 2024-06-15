from django import forms
from .models import Supplier, Item, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem
from django.forms.models import inlineformset_factory

class DateInput(forms.DateInput):
    input_type = 'date'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone_number', 'address', 'tin_number']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description', 'category', 'unit_of_measurement', 'current_unit_price', 'stock_balance', 'minimum_stock']

class PurchaseRecordForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecord
        fields = ['date', 'supplier', 'purchaser', 'voucher_number', 'upload_receipt']
        widgets = {
            'date': DateInput(),
        }

class PurchaseRecordItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecordItem
        fields = ['item', 'quantity', 'unit_price']
        widgets = {
            'unit_price': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.all()

class IssueRecordForm(forms.ModelForm):
    class Meta:
        model = IssueRecord
        fields = ['date', 'department', 'issued_by', 'received_by', 'voucher_number']
        widgets = {
            'date': DateInput(),
        }

class IssueRecordItemForm(forms.ModelForm):
    class Meta:
        model = IssueRecordItem
        fields = ['item', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.all()

PurchaseRecordItemFormSet = inlineformset_factory(
    PurchaseRecord, PurchaseRecordItem, form=PurchaseRecordItemForm, extra=1, can_delete=True
)

IssueRecordItemFormSet = inlineformset_factory(
    IssueRecord, IssueRecordItem, form=IssueRecordItemForm, extra=1, can_delete=True
)

class ItemFilterForm(forms.Form):
    description = forms.CharField(required=False, label='Description')
    category = forms.ChoiceField(choices=[('', 'All Categories')] + list(Item.CATEGORY_CHOICES), required=False, label='Category')
