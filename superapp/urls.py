from . import views
from django.urls import path


urlpatterns = [

    path("index/", views.index, name="index"),
    path("base", views.base, name="base"),
    path('index/<int:id>/item/',views.item,name='item'),
    path('kids/',views.kids,name='kids'),
    path('about/',views.about,name='about'),
    path('account/',views.account,name='account'),
    path('checkout/',views.checkout,name='checkout'),
    path('contacts/',views.contacts,name='contacts'),
    path('faq/',views.faq,name='faq'),
    path('goods_compare/',views.goods_compare,name='goods_compare'),
    path('index_header_fix/',views.index_header_fix,name='index_header_fix'),
    path('index_light_footer/',views.index_light_footer,name='index_light_footer'),
    path('privacy_policy/',views.privacy_policy,name='privacy_policy'),
    path('product_list/',views.product_list,name='product_list'),
    path('search_result/',views.search_result,name='search_result'),
    path('shopping_cart_null/',views.shopping_cart_null,name='shopping_cart_null'),
    path('shopping_cart/',views.shopping_cart,name='shopping_cart'),
    path('standard_forms/',views.standard_forms,name='standard_forms'),
    path('terms_conditions/',views.terms_conditions,name='terms_conditions'),
    path('wishlist/',views.wishlist ,name='wishlist'),
    path("update_items/", views.update_items, name="update_items")
]
