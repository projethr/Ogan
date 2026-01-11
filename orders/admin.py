from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html
from payment.models import Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['transaction_id', 'amount', 'status', 'created_at']
    can_delete = False

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'total_amount_display', 'status_badge', 'payment_status', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['id', 'full_name', 'phone', 'email']
    inlines = [OrderItemInline, PaymentInline]
    actions = ['mark_as_paid', 'mark_as_prepared', 'mark_as_delivered']
    
    fieldsets = (
        ('Informations Client', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city')
        }),
        ('Statut de la Commande', {
            'fields': ('status', 'is_paid')
        }),
    )

    def total_amount_display(self, obj):
        return format_html('<b>{} FCFA</b>', obj.get_total_cost())
    total_amount_display.short_description = 'Montant Total'

    def status_badge(self, obj):
        colors = {
            'pending': '#6b7280', # gray
            'paid': '#2563eb',    # blue
            'prepared': '#d97706', # amber
            'delivered': '#059669', # emerald
            'cancelled': '#dc2626', # red
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: bold; text-transform: uppercase;">{}</span>',
            colors.get(obj.status, '#000'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Statut'

    def payment_status(self, obj):
        if obj.is_paid:
            return format_html('<span style="color: green; font-weight: bold;">✔ Payée</span>')
        return format_html('<span style="color: red; font-weight: bold;">✘ Non payée</span>')
    payment_status.short_description = 'Paiement'

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid', is_paid=True)
    mark_as_paid.short_description = "✔ Valider le Paiement"

    def mark_as_prepared(self, request, queryset):
        queryset.update(status='prepared')
    mark_as_prepared.short_description = "📦 Marquer : En préparation"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = "🚚 Marquer : Livrée"
