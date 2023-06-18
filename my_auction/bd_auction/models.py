from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class User_buyer(models.Model):
    tg_id = models.IntegerField(blank=True)
    strike_count = models.IntegerField(blank=True)
    # ban_user = models.BooleanField(default=False)
    # wallet = models.IntegerField(blank=True, default=0)
    # good_buy = models.IntegerField(blank=True, default=0)



class Claim_message(models.Model):
    id_user = models.CharField(max_length=20)
    massage_text = models.TextField()
    finish_process = models.BooleanField(default=False)


class Lots(models.Model):
    name = models.CharField(max_length=100)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.CharField(max_length=15)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    publication = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    photo1 = models.ImageField(upload_to='img/%Y/%m/%d/', verbose_name="Фото 1")
    photo2 = models.ImageField(upload_to='img/%Y/%m/%d/', blank=True, verbose_name="Фото 2")
    photo3 = models.ImageField(upload_to='img/%Y/%m/%d/', blank=True, verbose_name="Фото 3")
    file_rar = models.FileField(upload_to='files/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Лот"
        verbose_name_plural = "Лоты"
        ordering = ['date_start']


class Lots_accept(models.Model):
    lot_id = models.OneToOneField(Lots, on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)


class Bets(models.Model):
    prise = models.CharField(max_length=100)
    date = models.DateTimeField()
    id_lot = models.ForeignKey('Lots', on_delete=models.PROTECT)
    id_user = models.CharField(max_length=20)

    def __str__(self):
        return self.id_lot

    class Meta:
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"


class InfoUser(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    username_tg = models.CharField(max_length=150, verbose_name='@username в Телеграм')
    wallet = models.IntegerField(blank=True, default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    tg_id = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Мнфо об {self.user_id}'

    class Meta:
        verbose_name = "Информация о пользователе"
        verbose_name_plural = "Информация о пользователях"


@receiver(post_save, sender=Lots)
def save_user_profile(sender, instance, **kwargs):
    try:
        Lots_accept.objects.get(lot_id=instance.id)
        pass
    except:
        lot_id = instance
        accept = Lots_accept(lot_id=lot_id)
        accept.save()
