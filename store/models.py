from django.db import models
from django.utils import timezone

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Beverage', 'Beverage'),
        ('Food Provision', 'Food Provision'),
        ('Sanitary', 'Sanitary'),
        ('Maintenance', 'Maintenance'),
        ('Service Aid', 'Service Aid'),
        ('Stationary', 'Stationary'),
        ('Sundry', 'Sundry'),
        ('Fresh Baazar', 'Fresh Baazar'),
    ]
    
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    unit_of_measurement = models.CharField(max_length=50)
    current_unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_balance = models.IntegerField()
    minimum_stock = models.IntegerField()
    
    def __str__(self):
        return self.description

class PurchaseRecord(models.Model):
    date = models.DateField(default=timezone.now)
    supplier = models.CharField(max_length=255)
    purchaser = models.CharField(max_length=255)
    upload_receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    
    def __str__(self):
        return f'Purchase Record {self.id} - {self.date}'
    
    def delete(self, using=None, keep_parents=False):
        for item in self.items.all():
            item.item.stock_balance -= item.quantity
            item.item.save()
        super().delete(using=using, keep_parents=keep_parents)

class PurchaseRecordItem(models.Model):
    purchase_record = models.ForeignKey(PurchaseRecord, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.item.current_unit_price = self.unit_price
        self.item.stock_balance += self.quantity
        self.item.save()
    
    def __str__(self):
        return f'{self.quantity} x {self.item.description}'

class IssueRecord(models.Model):
    date = models.DateField(default=timezone.now)
    department = models.CharField(max_length=255)
    issued_by = models.CharField(max_length=255)
    received_by = models.CharField(max_length=255)
    
    def __str__(self):
        return f'Issue Record {self.id} - {self.date}'
    
    def delete(self, using=None, keep_parents=False):
        for item in self.items.all():
            item.item.stock_balance += item.quantity
            item.item.save()
        super().delete(using=using, keep_parents=keep_parents)

class IssueRecordItem(models.Model):
    issue_record = models.ForeignKey(IssueRecord, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.unit_price = self.item.current_unit_price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.item.stock_balance -= self.quantity
        self.item.save()
    
    def __str__(self):
        return f'{self.quantity} x {self.item.description}'

