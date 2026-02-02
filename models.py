from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    description = models.TextField()
    stock = models.IntegerField()
    img_url = models.URLField(max_length=500) 

    def __str__(self):
        return self.pname
   
    class Meta:
        db_table = "product"