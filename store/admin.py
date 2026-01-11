from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'category', 'price', 'stock', 'colored_stock', 'is_active', 'updated_at']
    list_filter = ['category', 'is_active', 'created_at']
    list_editable = ['price', 'stock', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    actions = ['make_active', 'make_inactive']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:45px; border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    image_tag.short_description = 'Aperçu'

    def colored_stock(self, obj):
        if obj.stock <= 0:
            color = 'red'
            text = f"RUPTURE ({obj.stock})"
        elif obj.stock <= 5:
            color = 'orange'
            text = f"FAIBLE ({obj.stock})"
        else:
            color = 'green'
            text = obj.stock
        return format_html('<b style="color: {};">{}</b>', color, text)
    colored_stock.short_description = 'Stock'

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Activer les produits"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Désactiver les produits"
