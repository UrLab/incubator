from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category)
    stock_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Barcode(models.Model):
    product = models.ForeignKey("stock.Product")
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.code


class StockRefill(models.Model):
    """
    Represents a stock refilling event. Tracks who and when refilled the stock, uses ProductRefill in order
        to track each individual stock that was updated.
    """
    user = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL,
                             help_text="The person responsible for this stock refilling. \
                             Ideally the person who did the data entry after shopping")
    when = models.DateTimeField(default=timezone.now)
    updates = models.ManyToManyField(to="stock.Product", through="stock.ProductRefill",
                                     help_text="All the product stocks that were updated in this refill")

    def __str__(self):
        return "Stock refilled by {} on {}".format(self.user, self.when)


class ProductRefill(models.Model):
    """
    Many to many intermediary table used in order to store the product stock being updated with its quantity
    Regrouped in StockRefill.
    """
    refill = models.ForeignKey("stock.StockRefill", help_text="The refill that generated this update")
    product = models.ForeignKey("stock.Product", help_text="The product whose stock was refilled")
    amount = models.IntegerField(help_text="The quantity by which the stock was increased")

    def __str__(self):
        return "Refill of {} by {} unit(s)".format(self.product, self.amount)


class Transaction(models.Model):
    user = models.ForeignKey("users.User")
    when = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TransferTransaction(Transaction):
    receiver = models.ForeignKey("users.User", related_name="incoming_transfers")
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{} a transféré {}€ à {}".format(self.user, self.amount, self.receiver)


class TopupTransaction(Transaction):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    topup_type = models.CharField(
        max_length=20,
        choices=[
            ('BANK', "Virement"),
            ('CASH', "Caisse"),
        ],
    )

    def __str__(self):
        return "{} a versé {}€ sur son ardoise. ({})".format(self.user, self.amount, self.get_topup_type_display())


class ProductTransaction(Transaction):
    product = models.ForeignKey("stock.Product")

    def price(self):
        return self.product.price

    def __str__(self):
        return "{} a dépensé {}€ pour le produit {}".format(self.user, self.product.price, self.product)


class MiscTransaction(Transaction):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    info = models.TextField()

    def __str__(self):
        return "{} a dépensé {}€ pour {}".format(self.user, self.amount, self.info)
