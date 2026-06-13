from django.contrib import admin
from .models import PaymentMethod, Subscription, Payment, Invoice

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_number', 'is_active')
    list_filter = ('is_active',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('student', 'plan', 'start_date', 'end_date', 'status')
    list_filter = ('plan', 'status')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'student', 'amount', 'due_date', 'is_paid')
    list_filter = ('is_paid',)