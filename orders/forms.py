from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'city']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Votre nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Email (optionnel)'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': '0123456789'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Adresse de livraison'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Ville'}),
        }
