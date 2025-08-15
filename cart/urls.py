from . import views
from django . urls import path

urlpatterns = [
    path('add-to-cart/',views.add_to_cart, name="add-to-cart"),
    path('cart/<str:user_email>/', views.get_cart_items, name="get-cart-items"),
    path('remove-cart-item/', views.remove_cart_item, name="remove-cart-item"),
    path('update-cart-item-quantity/', views.update_cart_quantity, name="update_cart_item_quantity")
]
