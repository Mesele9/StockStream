from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import Item, PurchaseRecord, PurchaseRecordItem, IssueRecord, IssueRecordItem
from .forms import ItemForm, PurchaseRecordForm, PurchaseRecordItemFormSet, IssueRecordForm, IssueRecordItemFormSet


def dashboard(request):
    #items = Item.objects.all()
    recent_purchase_records = PurchaseRecord.objects.order_by('-date')[:5]
    recent_issue_records = IssueRecord.objects.order_by('-date')[:5]
    low_stock_items = Item.objects.filter(stock_balance__lt=F('minimum_stock'))
    
    context = {
        #'items': items,
        'recent_purchase_records': recent_purchase_records,
        'recent_issue_records': recent_issue_records,
        'low_stock_items': low_stock_items,
    }
    
    return render(request, 'store/dashboard.html', context)


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

def item_edit(request, pk):
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
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'store/item_confirm_delete.html', {'item': item})



def purchase_record_list(request):
    purchase_records = PurchaseRecord.objects.all()
    return render(request, 'store/purchase_record_list.html', {'purchase_records': purchase_records})

def purchase_record_detail(request, pk):
    purchase_record = get_object_or_404(PurchaseRecord, pk=pk)
    purchase_record_items = PurchaseRecordItem.objects.filter(purchase_record=purchase_record)
    return render(request, 'store/purchase_record_detail.html', {'purchase_record': purchase_record, 'purchase_record_items': purchase_record_items})


def purchase_record_create(request):
    if request.method == 'POST':
        form = PurchaseRecordForm(request.POST, request.FILES)
        formset = PurchaseRecordItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            purchase_record = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.purchase_record = purchase_record
                item.save()
            return redirect('purchase_record_list')
    else:
        form = PurchaseRecordForm()
        formset = PurchaseRecordItemFormSet()

    return render(request, 'store/purchase_record_form.html', {'form': form, 'formset': formset})


def purchase_record_edit(request, pk):
    purchase_record = get_object_or_404(PurchaseRecord, pk=pk)
    if request.method == 'POST':
        form = PurchaseRecordForm(request.POST, request.FILES, instance=purchase_record)
        formset = PurchaseRecordItemFormSet(request.POST, instance=purchase_record)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('purchase_record_list')
    else:
        form = PurchaseRecordForm(instance=purchase_record)
        formset = PurchaseRecordItemFormSet(instance=purchase_record)
    return render(request, 'store/purchase_record_form.html', {'form': form, 'formset': formset})


def purchase_record_delete(request, pk):
    purchase_record = get_object_or_404(PurchaseRecord, pk=pk)
    if request.method == 'POST':
        purchase_record.delete()
        return redirect('purchase_record_list')
    return render(request, 'store/purchase_record_confirm_delete.html', {'purchase_record': purchase_record})


def issue_record_list(request):
    issue_records = IssueRecord.objects.all()
    return render(request, 'store/issue_record_list.html', {'issue_records': issue_records})

def issue_record_detail(request, pk):
    issue_record = get_object_or_404(IssueRecord, pk=pk)
    issue_record_items = IssueRecordItem.objects.filter(issue_record=issue_record)
    return render(request, 'store/issue_record_detail.html', {'issue_record': issue_record, 'issue_record_items': issue_record_items})


def issue_record_create(request):
    if request.method == 'POST':
        form = IssueRecordForm(request.POST)
        formset = IssueRecordItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            issue_record = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.issue_record = issue_record
                item.save()
            return redirect('issue_record_list')
    else:
        form = IssueRecordForm()
        formset = IssueRecordItemFormSet()

    return render(request, 'store/issue_record_form.html', {'form': form, 'formset': formset})


def issue_record_edit(request, pk):
    issue_record = get_object_or_404(IssueRecord, pk=pk)
    if request.method == 'POST':
        form = IssueRecordForm(request.POST, instance=issue_record)
        formset = IssueRecordItemFormSet(request.POST, instance=issue_record)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('issue_record_list')
    else:
        form = IssueRecordForm(instance=issue_record)
        formset = IssueRecordItemFormSet(instance=issue_record)
    return render(request, 'store/issue_record_form.html', {'form': form, 'formset': formset})


def issue_record_delete(request, pk):
    issue_record = get_object_or_404(IssueRecord, pk=pk)
    if request.method == 'POST':
        issue_record.delete()
        return redirect('issue_record_list')
    return render(request, 'store/issue_record_confirm_delete.html', {'issue_record': issue_record})
