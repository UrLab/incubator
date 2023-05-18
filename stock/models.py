from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)
    when = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TransferTransaction(Transaction):
    receiver = models.ForeignKey(
        "users.User", related_name="incoming_transfers", on_delete=models.DO_NOTHING
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{} a transféré {}€ à {}".format(self.user, self.amount, self.receiver)


class TopupTransaction(Transaction):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    topup_type = models.CharField(
        max_length=20,
        choices=[
            ("BANK", "Virement"),
            ("CASH", "Caisse"),
        ],
    )

    def __str__(self):
        return "{} a versé {}€ sur son ardoise. ({})".format(
            self.user, self.amount, self.get_topup_type_display()
        )


class ProductTransaction(Transaction):
    product = models.ForeignKey("stock.Product", on_delete=models.DO_NOTHING)

    def price(self):
        return self.product.price

    def __str__(self):
        return "{} a dépensé {}€ pour le produit {}".format(
            self.user, self.product.price, self.product
        )


class MiscTransaction(Transaction):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    info = models.TextField()

    def __str__(self):
        return "{} a dépensé {}€ pour {}".format(self.user, self.amount, self.info)


class FundZone(models.Model):
    payment_method = (
        ("BANK", "Virement"),
        ("CASH", "Caisse"),
    )

    name = models.CharField(max_length=50)
    method = models.CharField(max_length=4, choices=payment_method)

    @property
    def balance(self):
        total = 0
        for payment in self.paymenttransaction_set.all():
            if payment.way == "a":
                total -= payment.amount
            else:
                total += payment.amount
        return total + sum(
            trans.amount
            for trans in TopupTransaction.objects.filter(topup_type=self.method)
        )

    @property
    def payments(self):
        return PaymentTransaction.objects.filter(zone=self).order_by("-payment_date")

    def __str__(self):
        return self.name


class PaymentTransaction(Transaction):
    ways = (
        ("a", "Dépense"),
        ("b", "Réception"),
    )

    amount = models.DecimalField(max_digits=6, decimal_places=2)
    way = models.CharField(max_length=1, default="a", choices=ways)
    receipt = models.FileField(upload_to="souches", null=True, blank=True)
    zone = models.ForeignKey(
        "stock.FundZone", on_delete=models.SET_NULL, null=True, blank=True
    )
    comments = models.CharField(max_length=200, null=True, blank=True)
    payment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.get_way_display()} d'un montant de {self.amount}€ vérifié par {self.user}"


class RefundTransaction(Transaction):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment = models.ForeignKey(
        "stock.PaymentTransaction", on_delete=models.CASCADE, null=True, blank=True
    )
    receipt = models.FileField(upload_to="souches", null=True, blank=True)

    @property
    def completed(self):
        return self.payment is not None

    def refund(self, zone: FundZone, user):
        """Completes a refund transaction

        Args:
            zone (FundZone): The zone from which the refund has been done
        """
        self.payment = PaymentTransaction.objects.create(
            user=user,
            amount=self.amount,
            way="a",
            receipt=self.receipt,
            zone=zone,
            comments=f"Remboursement '{self.title}' à {self.user.username}",
        )
        self.save()

    def __str__(self):
        if self.completed:
            return f"{self.user} a été remboursé {self.amount}€ pour {self.title}"
        return f"{self.user} demande {self.amount}€ de remboursement '{self.title}'"
