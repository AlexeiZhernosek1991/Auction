from django.db import models


class Lot(models.Model):
    name = models.CharField(max_length=100)
    seller_id = models.TextField()
    price = models.TextField()
    date_start = models.DateTimeField()
    date_finish = models.CharField()
    publication = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"
        ordering = ['name']


class Photo(models.Model):
    lot_id = models.ForeignKey('Lot', on_delete=models.PROTECT)

    def __str__(self):
        return self.lot_id

