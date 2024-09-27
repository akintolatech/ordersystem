from django.db import models


# Create your models here.
class Legal(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=2200)

    def __str__(self):
        return self.title


class Estate(models.Model):
    # fields for the estate object
    img = models.ImageField(upload_to="estates/", default="url")
    img2 = models.ImageField(upload_to="estates/", default="url")
    img3 = models.ImageField(upload_to="estates/", default="url")
    img4 = models.ImageField(upload_to="estates/", default="url")
    title = models.CharField(max_length=22)
    description = models.CharField(max_length=50, default="A very good house")
    area = models.CharField(max_length=22)
    inspection_fee = models.IntegerField(default=5000)
    agent_fee = models.IntegerField(default=10000)
    rental_fee = models.IntegerField(default=100000)

    # Derived model field for total price
    total_price = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate and set the total price before saving
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        # Calculate the total price based on fees
        return self.inspection_fee + self.agent_fee + self.rental_fee

    def __str__(self):
        return self.title
