from django.db      import models


class Country(models.Model):
    name = models.CharField(max_length = 100)
  
    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'countries'

class Region(models.Model):
    name = models.CharField(max_length = 200)
  
    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'regions'

class WineType(models.Model):
    name = models.CharField(max_length = 100)
  
    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'types'

class Style(models.Model):
    name = models.CharField(max_length = 200)
  
    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'styles'

class Winery(models.Model):
    name = models.CharField(max_length = 200)
  
    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'wineries'

class Distributor(models.Model):
    name = models.CharField(max_length = 200)
  
    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'distributors'

class Grape(models.Model):
    name = models.CharField(max_length = 100)
  
    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'grapes'

class Product(models.Model):
    name            = models.CharField(max_length = 150)
    image           = models.URLField(max_length = 500)
    country         = models.ForeignKey(Country, on_delete = models.CASCADE, related_name = 'products')
    region          = models.ForeignKey(Region, on_delete = models.CASCADE, related_name = 'products')
    wine_type       = models.ForeignKey(WineType, on_delete = models.CASCADE, related_name = 'products')
    winery          = models.ForeignKey(Winery, on_delete = models.CASCADE, related_name = 'products')
    style           = models.ForeignKey(Style, on_delete = models.CASCADE, related_name = 'products')
    distributor     = models.ForeignKey(Distributor, on_delete = models.CASCADE, related_name = 'products')
    alcohol_content = models.DecimalField(max_digits = 7, decimal_places = 2)
    allergen        = models.CharField(max_length = 150)
    highlight       = models.TextField()
    taste_summary   = models.CharField(max_length = 1000)
    bold            = models.DecimalField(max_digits = 7, decimal_places = 2)
    sweet           = models.DecimalField(max_digits = 7, decimal_places = 2)
    acidic          = models.DecimalField(max_digits = 7, decimal_places = 2)
    grape           = models.ManyToManyField(Grape, through = 'ProductGrape')

    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'products'

class ProductGrape(models.Model):
    product  = models.ForeignKey(Product, on_delete = models.CASCADE)
    grape    = models.ForeignKey(Grape, on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'products_grapes'

class Vintage(models.Model):
    product        = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'vintages')
    year           = models.IntegerField(default = 0)
    price          = models.DecimalField(max_digits = 10, decimal_places = 2)
    feature        = models.TextField(null = True)
    discount_rate  = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)
    edit_note      = models.TextField(null = True)
    description    = models.TextField(null = True)
    vin            = models.TextField(null = True)
    domaine        = models.TextField(null = True)
    vignoble       = models.TextField(null = True)
    stock          = models.IntegerField(default = 0)
    average_score  = models.FloatField(default = 0)
    total_rating   = models.IntegerField(default = 0)
    
    class Meta:
        db_table = 'vintages'

class Rating(models.Model):
    user        = models.ForeignKey('account.Account', on_delete = models.CASCADE, related_name = 'ratings')
    vintage     = models.ForeignKey(Vintage, on_delete = models.CASCADE, related_name = 'ratings')
    grade       = models.IntegerField(default = 0)
    
    class Meta:
        db_table = 'ratings'
