from django.contrib import admin
from . models import Brand, Category, Order, OrderCart, Product, MenuList, ProductCategory, ProductImage, UserPermission, ProductMainCategory, ProductSubCategory

# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(MenuList)
admin.site.register(UserPermission)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)

@admin.register(ProductMainCategory)
class ProductMainCategoryAdmin(admin.ModelAdmin):
    list_display         = ('main_cat_name', 'cat_slug', 'cat_ordering', 'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active')
    list_filter          = ('is_active',)
    search_fields        = ('main_cat_name', 'cat_slug')
    ordering             = ('cat_ordering',) 

@admin.register(ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display         = ('sub_cat_name', 'main_category', 'sub_cat_ordering', 'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active')
    list_filter          = ('is_active',)
    search_fields        = ('sub_cat_name', 'sub_cat_slug')
    ordering             = ('sub_cat_ordering',) 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'avl_quantity', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'brand')
    search_fields = ('name', 'slug', 'brand__name')
    ordering = ('name',)

admin.site.register(OrderCart)
admin.site.register(Order)