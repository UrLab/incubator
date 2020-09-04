from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)
    when = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TransferTransaction(Transaction):
    receiver = models.ForeignKey("users.User", related_name="incoming_transfers", on_delete=models.DO_NOTHING)
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
    product = models.ForeignKey("stock.Product", on_delete=models.DO_NOTHING)

    def price(self):
        return self.product.price

    def __str__(self):
        return "{} a dépensé {}€ pour le produit {}".format(self.user, self.product.price, self.product)


class MiscTransaction(Transaction):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    info = models.TextField()

    def __str__(self):
        return "{} a dépensé {}€ pour {}".format(self.user, self.amount, self.info)


class Payment(Transaction):
    payment_method = (
        ('a', 'Card'),
        ('b', 'Cash'),
    )

    amount = models.DecimalField(max_digits=6, decimal_places=2)
    method = models.CharField(max_length=1, choices=payment_method)
    picture = models.ImageField(upload_to='souches', null=True, blank=True)

    def __str__(self):
        return "Achat d'un montant de {} vérifié par {} ({})".format(self.amount, self.user, self.get_method_display())