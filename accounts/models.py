from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('sales_staff', 'Sales Staff'),
        ('customer_service', 'Customer Service'),
    ]
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales_staff')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # Add role foreign key
    user_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        role_name = self.user_role.name if self.user_role else self.get_role_display()
        return f"{self.get_full_name()} ({role_name})"