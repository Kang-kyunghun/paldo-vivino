from django.db      import models
from account.models import Account
from product.models import Vintage

class Cart(models.Model):
    user       = models.ForeignKey(Account, on_delete=models.CASCADE)
    vintage    = models.ForeignKey(Vintage, on_delete=models.CASCADE, related_name = 'carts')
    quantity   = models.IntegerField(default=1)
    
    class Meta:
        db_table = "carts"