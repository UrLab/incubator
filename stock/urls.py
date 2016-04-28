from django.conf.urls import patterns, url
from .views import product_infos, buy_product_with_stock_handler

urlpatterns = patterns(
    '',
    url(r'^product/(?P<product_barcode>.+)$', product_infos, name='product_infos'),
    url(r'^stock_handler$', buy_product_with_stock_handler, name='stock_handler_endpoint'),
)
