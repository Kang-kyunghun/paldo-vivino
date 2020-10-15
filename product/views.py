import json

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from utils                  import check_wishlist
from .models                import Product, Vintage, WineType, Country, Region, Style, Rating


class ProductsView(View):   
    def get(self, request):
        MINIMUM_RATING  = 0
        MAXIMUM_RATING  = 5
        MINIMUM_PRICE   = 0
        
        type_filter     = request.GET.getlist('type') 
        region_filter   = request.GET.getlist('region')
        country_filter  = request.GET.getlist('country')
        style_filter    = request.GET.getlist('style')
        rating_filter   = request.GET.get('rating', MINIMUM_RATING)
        price_low       = request.GET.get('price_low', MINIMUM_PRICE)
        price_high      = request.GET.get('price_high')
        order           = request.GET.get('order', 'id') 
        
        evaluation_condition = [
            {
                "filter_name" : type_filter,
                "object"      : WineType,
            },
            {
                "filter_name" : region_filter,
                "object"      : Region,
            },
            {
                "filter_name" : country_filter,
                "object"      : Country,
            },
            {
                "filter_name" : style_filter,
                "object"      : Style,
            },
        ]

        for condition in evaluation_condition:
            if  (condition['filter_name'] and 
                not condition['object'].objects.filter(name__in = condition['filter_name']).exists()):
                return JsonResponse({'message': 'INVALID_VALUE'}, status=400)
        
        if  float(rating_filter) < MINIMUM_RATING or float(rating_filter) > MAXIMUM_RATING:
            return JsonResponse({'message': 'INVALID_VALUE'}, status=400)  
        
        if  float(price_low) < MINIMUM_PRICE:
            return JsonResponse({'message': 'INVALID_VALUE'}, status=400)
        
        filter_factor ={
            'product__wine_type__name__in' : type_filter,
            'price__lte'                   : price_high,
            'price__gte'                   : price_low,
            'average_score__gte'           : rating_filter,
            'product__region__name__in'    : region_filter,
            'product__country__name__in'   : country_filter,
            'product__style__name__in'     : style_filter
        }
        applied_filter={key : value for key, value in filter_factor.items() if value}
    
        wines = Vintage.objects.select_related('product__winery', 
                                            'product__country', 
                                            'product__region',
                                            'product__wine_type').filter(**applied_filter).order_by(order)
        products = {
            "count"  : wines.count(),
            "result" : [{
                            "id"          : wine.id,
                            "image_url"   : wine.product.image,
                            "type"        : wine.procuct.wine_type.name,
                            "winery"      : wine.product.winery.name,
                            "wine_name"   : wine.product.name,
                            "year"        : wine.year,
                            "nation"      : wine.product.country.name,
                            "region"      : wine.product.region.name,
                            "rating"      : wine.average_score,
                            "ratings"     : wine.total_rating,
                            "price"       : wine.price,
                            "percentage"  : wine.discount_rate,
                            "feature"     : wine.feature,
                            "editor_note" : wine.edit_note
                        } for wine in wines]
        }
        return JsonResponse({'products': products}, status=200)

class ProductView(View):
    def get(self, request, id):
        try:
            wine = Vintage.objects.select_related('product__winery', 
                                                'product__country', 
                                                'product__region',
                                                'product__distributor').get(id = id)
            product = {
                    "id"              : wine.id,
                    "image_url"       : wine.product.image,
                    "type"            : wine.product.wine_type.name,
                    "winery"          : wine.product.winery.name,
                    "wine_name"       : wine.product.name,
                    "year"            : wine.year,
                    "nation"          : wine.product.country.name,
                    "region"          : wine.product.region.name,
                    "rating"          : wine.average_score,
                    "ratings"         : wine.total_rating,
                    "price"           : wine.price,
                    "percentage"      : wine.discount_rate,
                    "feature"         : wine.feature,
                    "editor_note"     : wine.edit_note,
                    "merchant"        : wine.product.distributor.name,
                    "description"     : [wine.description, wine.vin, wine.domaine, wine.vignoble],
                    "highlight"       : wine.product.highlight.split('\u2028'),
                    "taste_summary"   : wine.product.taste_summary,
                    "bold"            : wine.product.bold,
                    "sweet"           : wine.product.sweet,
                    "acidic"          : wine.product.acidic,
                    "score"           : [Rating.objects.filter(vintage_id = wine.id, grade = grade).count()for grade in range(5,0,-1)],
                    "wishlist"        : check_wishlist(request, id),
                    "grape"           : [grape.name for grape in wine.product.grape.all()],
                    "alcohol_content" : wine.product.alcohol_content,
                    "allergen"        : wine.product.allergen,
                    "vintages"      : [{
                                        "id"          : vintage.id,
                                        "year"        : vintage.year,
                                        "rating"      : vintage.average_score,
                                        "ratings"     : vintage.total_rating,
                                        "price"       : vintage.price,
                                        "percentage"  : vintage.discount_rate,
                                        "feature"     : vintage.feature,

                                        }for vintage in wine.product.vintages.order_by('-year')]
                }            
            return JsonResponse({'product': product}, status=200)  
        except ObjectDoesNotExist:
            return JsonResponse({'message':'ObjectDoesNotExist'}, status= 400)    