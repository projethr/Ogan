from django.db import models
from orders.models import Order

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    )
    
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    provider_reference = models.CharField(max_length=100, blank=True, null=True) # ID from MoMo

    def __str__(self):
        return f'Payment {self.transaction_id} for Order {self.order.id}'
