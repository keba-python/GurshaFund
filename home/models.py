from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator


# Create your models here.
STATUS_TYPE = (
    ('pending','Pending'),
    ('completed','Completed'),
    ('refunded','Refunded')

)

class Campaign(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10,decimal_places=2)
    current_amount = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category',on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titile 
    
class Donation(models.Model):
    amount = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0.01)])
    campaign = models.ForeignKey('Campaign',on_delete=models.CASCADE)
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default = False)
    message = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=20, choices=STATUS_TYPE,default='pending')
    transaction_id = models.CharField(max_length=100,blank=True,null=True)
    payment_method = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return f"{self.amount} donated to {self.campaign.title} by {self.donor.username}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    

