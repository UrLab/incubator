from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db.models import F

from stock.models import ProductRefill


@receiver(post_save, sender="stock.ProductRefill")
def increase_product_stock_on_refill_create(instance, created, **kwargs):
    """
    Signal responsible for the automatic updating of a product's stock when a ProductRefill object created
        during the process of creating a StockRefill objectself.

    A signal is used since we want it to be imperative that the creation of a ProductRefill entry increases
        the corresponding products stock.
    """
    if not created:
        # If this object wasnt newly created will shall let the pre_save signal take care of any updating.
        return

    product = instance.product
    stock_increase = instance.amount
    product.stock_amount += F("stock_amount") + stock_increase
    product.save()


@receiver(pre_save, sender="stock.ProductRefill")
def update_product_stock_on_refill_change(instance, **kwargs):
    """
    Signal responsible for the updating the stock_amount of the corresponding product to match any
        modifications to the ProductRefill object.
    """
    if instance.pk is None:
        # The model is being created, not updated so we let the post_save signal take care of it
        return

    old_version = ProductRefill.objects.get(pk=instance.pk)
    old_product = old_version.product
    new_product = instance.product
    old_amount = old_version.amount
    new_amount = instance.amount

    product_changed = new_product != old_product
    amount_changed = new_amount != old_amount

    if product_changed and amount_changed:
        # Decrease amount of old product object with old amount
        #   and
        # Increase amount of new product object with new amount
        old_product.stock_amount = F("stock_amount") - old_amount
        new_product.stock_amount = F("stock_amount") + new_amount
    elif product_changed:
        # Decrease amount of old product object with the current amount
        #   and
        # Increase amount of new product object with current amount
        old_product.stock_amount = F("stock_amount") - new_amount
        new_product.stock_amount = F("stock_amount") + new_amount
    elif amount_changed:
        # Update stock amount on the corresponding product object
        amount_delta = new_amount - old_amount
        new_product.stock_amount = F("stock_amount") + amount_delta

    old_product.save()
    new_product.save()


@receiver(post_delete, sender="stock.ProductRefill")
def update_product_stock_on_refill_delete(instance, **kwargs):
    """
    Signal responsible for decreasing the stock of a product if a stock refill of that product was deleted
    """
    instance.product.stock_amount = F("stock_amount") - instance.amount
    instance.product.save()
