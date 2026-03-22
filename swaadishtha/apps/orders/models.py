from django.db import models
import uuid


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'
        REFUNDED = 'REFUNDED', 'Refunded'
        RETURNED = 'RETURNED', 'Returned'
        FAILED = 'FAILED', 'Failed'
        PAYMENT_PENDING = 'PAYMENT_PENDING', 'Payment Pending'
        PAYMENT_FAILED = 'PAYMENT_FAILED', 'Payment Failed'
        PAYMENT_COMPLETED = 'PAYMENT_COMPLETED', 'Payment Completed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')  # was 'users.User'
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)  # was missing .choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['order_status']),
        ]

    def __str__(self):
        return f"Order {self.id} — {self.user.email}"


class OrderProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE, related_name='order_products')
    product_rate = models.DecimalField(max_digits=10, decimal_places=2)   # unit price at time of purchase
    product_qty = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)        # product_rate × product_qty
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Order Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return f"{self.product_variant.sku} × {self.product_qty} (Order {self.order.id})"


class OrderAddressType(models.TextChoices):
    SHIPPING = 'shipping', 'Shipping'
    BILLING = 'billing', 'Billing'


class OrderAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_addresses')
    address_type = models.CharField(max_length=20, choices=OrderAddressType.choices)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Order Addresses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order', 'address_type']),
        ]

    def __str__(self):
        return f"{self.address_type.title()} — {self.address_line1}, {self.city}"


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'


class PaymentInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_gateway = models.CharField(max_length=100)    # e.g. Razorpay, Stripe
    payment_method = models.CharField(max_length=100)     # e.g. UPI, card, netbanking
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    gateway_transaction_id = models.CharField(max_length=255, blank=True)  # ID from payment gateway
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Payment Info'
        indexes = [
            models.Index(fields=['payment_status']),
            models.Index(fields=['gateway_transaction_id']),
        ]

    def __str__(self):
        return f"{self.payment_gateway} — {self.payment_status} — Order {self.order.id}"


class InvoiceNumbering(models.Model):
    """Tracks the running invoice counter per financial year."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    financial_year = models.CharField(max_length=20, unique=True)   # e.g. "2025-26"
    invoice_prefix = models.CharField(max_length=20)                # e.g. "INV"
    last_invoice_number = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Invoice Numbering'

    def __str__(self):
        return f"{self.invoice_prefix} / {self.financial_year}"


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True)   # e.g. "INV-2025-26-0042"
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Invoices'
        indexes = [
            models.Index(fields=['invoice_number']),
        ]

    def __str__(self):
        return self.invoice_number
