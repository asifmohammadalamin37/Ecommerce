from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.text import slugify

# Create your models here.

class MenuList(models.Model):
    module_name        = models.CharField(max_length=100, db_index=True)
    menu_name          = models.CharField(max_length=100, unique=True, db_index=True)
    menu_url           = models.CharField(max_length=250, unique=True)
    menu_icon          = models.CharField(max_length=250, blank=True, null=True)
    parent_id          = models.IntegerField()
    is_main_menu       = models.BooleanField(default=False)
    is_sub_menu        = models.BooleanField(default=False)
    is_sub_child_menu  = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(blank=True, null=True)
    deleted_at         = models.DateTimeField(blank=True, null=True)
    created_by         = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active          = models.BooleanField(default=True)
    deleted            = models.BooleanField(default=False)

    class Meta:
        db_table = "menu_list"

    def __str__(self) -> str:
        return self.menu_name

class UserPermission(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_user_for_permission") 
    menu          = models.ForeignKey(MenuList, on_delete=models.CASCADE, related_name="menu_for_permission") 
    can_view      = models.BooleanField(default=False)
    can_add       = models.BooleanField(default=False)
    can_update    = models.BooleanField(default=False)
    can_delete    = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by_user") 
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_by_user", blank=True, null=True) 
    deleted_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deleted_by_user", blank=True, null=True)
    is_active     = models.BooleanField(default=True)
    deleted       = models.BooleanField(default=False)

    class Meta:
        db_table = "user_permission"

    def __str__(self):
        return str(self.menu)

class Brand(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brand'
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category'

class ProductMainCategory(models.Model):
    main_cat_name = models.CharField(max_length=100, unique=True)
    cat_slug      = models.SlugField(max_length=150, unique=True, blank=True)
    cat_image     = models.ImageField(upload_to='ecommerce/category_images/', blank=True, null=True)
    description   = models.TextField(blank=True, null=True)
    cat_ordering  = models.IntegerField(default=0,blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_created_by')
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_updated_by', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_active     = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_main_category'
        verbose_name_plural = 'Product Categories'
        ordering = ['-is_active','cat_ordering']

    def __str__(self):
        return self.main_cat_name
    
    def save(self, *args, **kwargs):
        if not self.cat_slug and self.main_cat_name:
            base_slug = slugify(self.main_cat_name)
            slug = base_slug
            num = 1
            while ProductMainCategory.objects.filter(cat_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.cat_slug = slug
        super().save(*args, **kwargs)
    
class ProductSubCategory(models.Model):
    main_category = models.ForeignKey(ProductMainCategory, on_delete=models.CASCADE, related_name='sub_categories')
    sub_cat_name = models.CharField(max_length=100, unique=True)
    sub_cat_slug      = models.SlugField(max_length=150, unique=True, blank=True)
    sub_cat_image     = models.ImageField(upload_to='ecommerce/sub_category_images/', blank=True, null=True)
    sub_cat_ordering  = models.IntegerField(default=0)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_category_created_by')
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_category_updated_by', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_active     = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_sub_category'
        verbose_name_plural = 'Product Sub Categories'
        ordering = ['-is_active','sub_cat_ordering']

    def __str__(self):
        return self.sub_cat_name
    
    def save(self, *args, **kwargs):
        if not self.sub_cat_slug and self.sub_cat_name:
            base_slug = slugify(self.sub_cat_name)
            slug = base_slug
            num = 1
            while ProductSubCategory.objects.filter(sub_cat_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.sub_cat_slug = slug
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    dimensions = models.CharField(max_length=255, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    delivery_day_min = models.PositiveIntegerField(default=0)
    delivery_day_max = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_reviews = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    avl_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'products'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='product_images/')
    position = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    
    class Meta:
        db_table = 'product_images'
        ordering = ['position']

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_products')

    def __str__(self):
        return f"{self.product.name} in {self.category.name}"
    
    class Meta:
        db_table = 'product_category'

class Attribute(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'attribute'

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
    
    class Meta:
        db_table = 'attribute_value'

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attributes')
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, related_name='attribute_products')

    def __str__(self):
        return f"{self.product.name} - {self.attribute_value}"
    
    class Meta:
        db_table = 'product_attribute_value'

class Membership(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'membership'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    @property
    def name(self):
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'customer'

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.product.name} - {self.rating}"
    
    class Meta:
        db_table = 'review'

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.customer.name}"
    
    class Meta:
        db_table = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.customer.name}'s cart"
    
    class Meta:
        db_table = 'cart_item'

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist for {self.customer.name}"
    
    class Meta:
        db_table = 'wishlist'

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.customer.name}'s wishlist"
    
    class Meta:
        db_table = 'wishlist_item'

class DiscountCoupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    
    class Meta:
        db_table = 'discount_coupons'

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=20, unique=True, blank=True, default='')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount_coupon = models.ForeignKey(DiscountCoupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} for {self.customer.name}"
    
    class Meta:
        db_table = 'order'

    def save(self, *args, **kwargs):
        if not self.order_number or self.order_number == '':
            current_year = datetime.date.today().year
            current_month = datetime.date.today().month
            current_day = datetime.date.today().day
            current_customer_id = self.customer.id

            last_order = Order.objects.filter(order_number__startswith=f"{current_year}{current_month:02d}{current_day:02d}").order_by('id').last()
            increase_number = 1
            new_order_number = f"{current_year}{current_month:02d}{current_day:02d}{current_customer_id:04d}{increase_number:04d}"

            while Order.objects.filter(order_number=new_order_number).exists():
                increase_number += 1
                new_order_number = f"{current_year}{current_month:02d}{current_day:02d}{current_customer_id:04d}{increase_number:04d}"
            
            self.order_number = new_order_number
        super().save(*args, **kwargs)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
    
    class Meta:
        db_table = 'order_details'

class OrderCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='order_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_order= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return_value=float(self.quantity) * float(self.product.price)
        return return_value
    
    class Meta:
        db_table = 'order_cart'

    def __str__(self):
        return f"{self.customer} - {self.product.name} ({self.quantity})"

class OnlinePaymentRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status_list = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    payment_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_requests_created')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment Request for Order #{self.order.id} - {self.payment_method}"
    
    class Meta:
        db_table = 'online_payment_request'

class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.payment_method}"
    
    class Meta:
        db_table = 'order_payments'

class OrderReturn(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns')
    reason = models.TextField(blank=True, null=True)
    status_list = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, default='pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return for Order #{self.order.id} - {self.status}"
    
    class Meta:
        db_table = 'order_return'

class OrderReturnDetail(models.Model):
    order_return = models.ForeignKey(OrderReturn, on_delete=models.CASCADE, related_name='return_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='return_details')
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return Detail for Order #{self.order_return.order.id} - {self.product.name}"
    
    class Meta:
        db_table = 'order_return_details'

class OrderRefund(models.Model):
    order_return = models.ForeignKey(OrderReturn, on_delete=models.CASCADE, related_name='refunds')
    refund_method = models.CharField(max_length=50)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Refund for Order #{self.order_return.order.id} - {self.refund_method}"
    
    class Meta:
        db_table = 'order_refunds'
    
class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def is_expired(self):
        return datetime.timezone.now() > self.created_at + datetime.timezone.timedelta(minutes=60)

    def __str__(self):
        return f"{self.email} - {self.code}"