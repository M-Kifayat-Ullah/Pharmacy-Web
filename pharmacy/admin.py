from django.contrib import admin
from .models import Medicine, Invoice, SaleItem

admin.site.register(Medicine)
admin.site.register(Invoice)
admin.site.register(SaleItem)