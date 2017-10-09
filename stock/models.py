from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey("users.User")
    when = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TransferTransaction(Transaction):
    receiver = models.ForeignKey("users.User", related_name="incoming_transfers")
    amount = models.DecimalField(max_digits=6, decimal_places=2)


class TopupTransaction(Transaction):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    topup_type = models.CharField(
        max_length=20,
        choices=[
            ('BANK', "Virement"),
            ('CASH', "Caisse"),
        ],
    )


class ProductTransaction(Transaction):
    product = models.ForeignKey("stock.Product")


class MiscTransaction(Transaction):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    info = models.TextField()
