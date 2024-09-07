from django.db import models
from django.contrib.auth.hashers import make_password


class Users(models.Model):
    GENDER_CHOICES = [
        ('M', 'ЭР'),
        ('F', 'ЭМ'),
    ]

    TCUSERNAME = models.CharField(help_text="Хэрэглэгчийн нэр", max_length=100, blank=False)
    TCPASSWORD = models.CharField(help_text="Нууц үг", max_length=100, blank=False)
    TCGENDER = models.CharField(
        help_text="Хүйс",
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',
        blank=False
    )
    TCEMAIL = models.CharField(help_text="Имэйл хаяг", max_length=100, blank=False, unique=True)

    def save(self, *args, **kwargs):
        # Ensure the password is hashed before saving
        if not self.TCPASSWORD.startswith('pbkdf2_'):  # To avoid re-hashing if the password is already hashed
            self.TCPASSWORD = make_password(self.TCPASSWORD)
        super(Users, self).save(*args, **kwargs)

    def __str__(self):
        return self.TCUSERNAME


class InfoSector(models.Model):
    sectorId = models.CharField(max_length=255, unique=True)  # String field for id
    name = models.CharField(max_length=255)  # String field for name
    isMain = models.BooleanField(default=False)  # Boolean field for isMain
    address = models.CharField(max_length=255)  # String field for address
    phone = models.DecimalField(max_digits=10, decimal_places=0)  # Decimal field for phone
    createdDate = models.DateTimeField(auto_now_add=True)  # DateTime field for createdDate

    def __str__(self):
        return self.name


class InfoProduct(models.Model):
    itemCode = models.DecimalField(max_digits=20, decimal_places=0, unique=True)  # Decimal field for item code
    itemName = models.CharField(max_length=255)  # String field for item name
    itemBillName = models.CharField(max_length=255)  # String field for shortened item name
    itemPrice = models.DecimalField(max_digits=20, decimal_places=2)  # Decimal field for item price
    isActive = models.BooleanField(default=True)  # Boolean field for active status
    createdDate = models.DateTimeField(auto_now_add=True)  # DateTime field for created date

    def __str__(self):
        return self.itemName


class History(models.Model):
    UserPk = models.ForeignKey(Users, on_delete=models.CASCADE)  # ForeignKey to the User model
    # infoProducts = models.ManyToManyField('InfoProduct')  # Many-to-Many relationship with InfoProduct
    infoOutSector = models.ForeignKey('InfoSector', on_delete=models.CASCADE,  related_name='out_sector_histories', limit_choices_to={'isMain': True}, default=1)
    infoToSector = models.ForeignKey('InfoSector', on_delete=models.CASCADE, related_name='to_sector_histories', default=1)  # ForeignKey to InfoSector, limited to only main sectors
    totalPrice = models.DecimalField(max_digits=20, decimal_places=2)  # Decimal field for total price
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional String field for description
    isIncome = models.BooleanField(default=True)  # Boolean field for income status
    createdDate = models.DateTimeField(auto_now_add=True)  # DateTime field for created date

    def __str__(self):
        return f"History {self.pk} - {self.UserPk.TCUSERNAME}"


class HistoryProduct(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE)  # Link to History
    product = models.ForeignKey(InfoProduct, on_delete=models.CASCADE)  # Link to InfoProduct
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)  # Field to store product count

    def __str__(self):
        return f"{self.product.itemName} - {self.quantity} pcs"
