from django.test import TestCase
from django.contrib.auth.models import User
from .models import Customer, Order
import datetime

class OrderTestCase(TestCase):
    def setUp(self):
        # Create a test user and customer
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(user=self.user)

    def test_order_number_generation(self):
        """Test that order_number is automatically generated when saving an Order"""
        order = Order.objects.create(
            customer=self.customer,
            order_amount=100.00,
            paid_amount=100.00,
            grand_total=100.00,
        )
        
        # Check that order_number is not empty
        self.assertNotEqual(order.order_number, '')
        self.assertIsNotNone(order.order_number)
        
        # Check that order_number follows the expected format
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        current_day = datetime.date.today().day
        
        # Format: YYYYMMDD{CUSTOMER_ID:04d}{SEQUENCE:04d}
        expected_prefix = f"{current_year}{current_month:02d}{current_day:02d}{self.customer.id:04d}"
        self.assertTrue(order.order_number.startswith(expected_prefix))
        
        print(f"Generated order number: {order.order_number}")
