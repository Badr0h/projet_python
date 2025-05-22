from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Item, ItemImage

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "Aucune image"
    preview.short_description = 'Aperçu'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price_per_day', 'available', 'owner', 'created_at')
    list_filter = ('category', 'available', 'condition', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    list_editable = ('available', 'price_per_day')
    inlines = [ItemImageInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
