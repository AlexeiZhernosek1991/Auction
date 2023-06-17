from django.contrib.sites import requests
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Lots(models.Model):
    name = models.CharField(max_length=100)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.CharField(max_length=15)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    publication = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    sold = models.BooleanField(default=False)
    photo1 = models.ImageField(upload_to='img/%Y/%m/%d/', blank=True, verbose_name="Фото 1")
    photo2 = models.ImageField(upload_to='img/%Y/%m/%d/', blank=True, verbose_name="Фото 2")
    photo3 = models.ImageField(upload_to='img/%Y/%m/%d/', blank=True, verbose_name="Фото 3")
    file_rar = models.FileField(upload_to='files/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Лот"
        verbose_name_plural = "Лоты"
        ordering = ['date_start']


class Bets(models.Model):
    prise = models.CharField(max_length=100)
    date = models.DateTimeField()
    id_lot = models.ForeignKey('Lots', on_delete=models.PROTECT)
    id_user = models.TextField(max_length=100)

    def __str__(self):
        return self.id_lot

    class Meta:
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"


@receiver(pre_save, sender=Lots)  # декоратор с сигналом перед сохранением для модели ORDERS
def f(sender, instance, **kwargs,):
    print(sender)
    print(instance)
