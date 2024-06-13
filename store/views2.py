from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem
from .forms import ItemForm, PurchaseRecordForm, PurchaseRecordItemForm, IssueRecordForm, IssueRecordItemForm
from django.forms import modelformset_factory


def item_list(request):
    items = Item.objects.all()
    return render(request, 'store/item_list.html', {'items': items})

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'store/item_form.html', {'form': form})

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'store/item_form.html', {'form': form})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'store/item_confirm_delete.html', {'item': item})


def purchase_record_create(request):
    PurchaseRecordItemFormSet = modelformset_factory(PurchaseRecordItem, fields=('item', 'quantity', 'unit_price',), extra=1)
    
    if request.method == 'POST':
        form = PurchaseRecordForm(request.POST, request.FILES)
        formset = PurchaseRecordItemFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            purchase_record = form.save()
            for form in formset:
                purchase_record_item = form.save(commit=False)
                purchase_record_item.purchase_record = purchase_record
                purchase_record_item.save()
                
                # Update the item's stock balance
                item = purchase_record_item.item
                item.stock_balance += purchase_record_item.quantity
                item.save()
                
            return redirect('purchase_record_list')
    else:
        form = PurchaseRecordForm()
        formset = PurchaseRecordItemFormSet(queryset=PurchaseRecordItem.objects.none())
    
    return render(request, 'store/purchase_record_form.html', {'form': form, 'formset': formset})


def issue_record_create(request):
    if request.method == 'POST':
        form = IssueRecordForm(request.POST)
        if form.is_valid():
            issue_record = form.save()
            for item_form in request.POST.getlist('items'):
                item_instance = IssueRecordItem(issue_record=issue_record, **item_form)
                item_instance.save()
            return redirect('issue_record_list')
    else:
        form = IssueRecordForm()
        item_form = IssueRecordItemForm()
    return render(request, 'store/issue_record_form.html', {'form': form, 'item_form': item_form})


# View for listing purchase records
def purchase_record_list(request):
    purchase_records = PurchaseRecord.objects.all()
    return render(request, 'store/purchase_record_list.html', {'purchase_records': purchase_records})

# View for listing issue records
def issue_record_list(request):
    issue_records = IssueRecord.objects.all()
    return render(request, 'store/issue_record_list.html', {'issue_records': issue_records})
