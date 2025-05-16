from django.urls import path, include
from carts import views

urlpatterns = [
    path('getCartItems/', views.get_cart_item),
    path('creationOfItem/', views.add_to_cart),
    path('updateItem/<int:pk>', views.update_cart_item),
    path('deleteItem/<int:pk>', views.delete_cart_item),
]
