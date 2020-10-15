from django.db      import models

class Account(models.Model):
    email             = models.CharField(max_length=100)
    first_name        = models.CharField(max_length=50)
    last_name         = models.CharField(max_length=50)
    password          = models.CharField(max_length=500)
    image             = models.URLField(max_length = 1000, null = True) 
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.last_name

    class Meta:
        db_table = "accounts"

class WishList(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    vintage = models.ForeignKey('product.Vintage', on_delete=models.CASCADE)
  
    class Meta:
        db_table = 'wishlists'
