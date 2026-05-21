from django.db import models


class Category(models.Model):
    categoryName  = models.CharField(max_length=255)
    categoryImage = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categoryName
