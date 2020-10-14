import json

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ObjectDoesNotExist

from utils                  import login_decorator
from .models                import Cart
from account.models         import Account, WishList
from product.models         import Vintage, Product

class CartsView(View):
    @login_decorator
    def get(self, request):
        carts = Cart.objects.select_related('vintage__product').filter(user_id = request.user_id)
        cart_list = {
            "count"  : carts.count(),
            "result" : [{
                            "id"         : cart.id,
                            "image_url"  : cart.vintage.product.image,
                            "winery"     : cart.vintage.product.winery.name,
                            "wine_name"  : cart.vintage.product.name,
                            "year"       : cart.vintage.year,
                            "nation"     : cart.vintage.product.country.name,
                            "region"     : cart.vintage.product.region.name,
                            "rating"     : cart.vintage.average_score,
                            "ratings"    : cart.vintage.total_rating,
                            "price"      : cart.vintage.price,
                            "percentage" : cart.vintage.discount_rate,
                            "feature"    : cart.vintage.feature,
                            "quantity"   : cart.quantity
                        } for cart in carts]
        }
        return JsonResponse({'cart_list': cart_list}, status=200)
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if Cart.objects.filter(user_id = request.user_id).filter(vintage_id = data['vintage_id']).exists():
                cart = Cart.objects.filter(user_id = request.user_id).get(vintage_id = data['vintage_id'])
                cart.quantity += data['quantity']
                cart.save()
                return JsonResponse({'message':'CHANGE_SUCCESS'}, status=200)
            else:
                Cart.objects.create(
                    user_id    = request.user_id,
                    vintage_id = data['vintage_id'],  
                    quantity   = data['quantity']
                )
                return JsonResponse({'message':'ADD_SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)

    @login_decorator
    def patch(self,request):
        try:
            data          = json.loads(request.body)
            cart          = Cart.objects.get(id = data['id'])
            cart_quantity = cart.quantity
            cart.quantity = int(data['quantity'])
            cart.save()
            patched_cart = {
                    "cart_id"        : cart.id,
                    "befor_quantity" : cart_quantity,
                    "after_quantity" : cart.quantity
            }
            return JsonResponse({'patch':patched_cart}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)
        except ObjectDoesNotExist:
            return JsonResponse({'message':'CART_DOES_NOT_EXIST'}, status=400)

    @login_decorator
    def delete(self, request, id):  
        try:
            if Cart.objects.get(id = id).user_id != request.user_id:
                return JsonResponse({'message':'INVALID_USER'}, status=403)
            
            if Cart.objects.filter(id = id).exists():
                Cart.objects.get(id = id).delete()
                return JsonResponse({'message':'SUCCESS'}, status=200)
            
        except ObjectDoesNotExist:
            return JsonResponse({'message':'CART_DOES_NOT_EXIST'}, status=400)