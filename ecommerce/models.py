from django.db import models
from django.utils import timezone
from authentication.models import User


class EcommerceUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='ecommerce')

class EcommerceUser(User):
    is_buyer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_shiper = models.BooleanField(default=False)

    objects = EcommerceUserManager()

    class Meta:
        verbose_name = "Ecommerce User"
        verbose_name_plural = "Ecommerce Users"

    def __str__(self):
        return f"{self.username}"

class Shop(models.Model):
    name = models.CharField(max_length=100)
    seller = models.ForeignKey(EcommerceUser, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} (seller: {self.seller})"

class Product(models.Model):
    name = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}(shop: {self.shop})"

class Cart(models.Model):
    buyer = models.ForeignKey(EcommerceUser, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart: {self.id} (buyer: {self.buyer}, shop: {self.shop})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} (quantity: {self.quantity}, cart: {self.cart})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('created', 'Created'),
        ('preparing', 'Preparing'),
        ('ready_to_ship', 'Ready to Ship'),
        ('shipped', 'Shipped'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    buyer = models.ForeignKey(EcommerceUser, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order: {self.id} (buyer: {self.buyer}, shop: {self.shop}, status: {self.status})"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()