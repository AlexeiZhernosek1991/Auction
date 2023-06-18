from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from Bot.send import send_


class Reg_tg(models.Model):
    username = models.CharField(max_length=200)
    id_tg = models.CharField(max_length=200)

    def __str__(self):
        return f'Для регистрации {self.username}'

    class Meta:
        verbose_name = "Для регистрации в тг"
        verbose_name_plural = "Для регистрации в тг"


class InfoUser(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    username_tg = models.CharField(max_length=150, verbose_name='@username в Телеграм')
    wallet = models.IntegerField(blank=True, default=0)
    tg_id = models.CharField(max_length=20, blank=True)
    ban_user = models.BooleanField(default=True)

    def __str__(self):
        return f'Инфо об {self.user_id}'

    class Meta:
        verbose_name = "Информация о пользователе"
        verbose_name_plural = "Информация о пользователях"


class User_buyer(models.Model):
    tg_id = models.CharField(max_length=200, blank=True)
    strike_count = models.IntegerField(blank=True)
    ban_user = models.BooleanField(default=False)
    wallet = models.IntegerField(blank=True, default=0)
    good_buy = models.IntegerField(blank=True, default=0)
    bet = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'Покупатель {self.tg_id}'

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Claim_message(models.Model):
    id_user = models.CharField(max_length=20, verbose_name='Укажите ваш логин')
    massage_text = models.TextField()
    finish_process = models.BooleanField(default=False)

    def __str__(self):
        return f'Сообщение {self.id_user}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Bets(models.Model):
    prise = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    auction_id = models.ForeignKey('Lots', on_delete=models.PROTECT)
    id_user = models.CharField(max_length=20)
    won = models.BooleanField(default=False)

    def __str__(self):
        return self.id_user

    class Meta:
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"


class Lots(models.Model):
    name = models.CharField(max_length=100)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
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


class Auction(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.PROTECT)
    lot_id = models.ForeignKey(Lots, on_delete=models.PROTECT)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    publication = models.BooleanField(default=False)
    price = models.CharField(max_length=15)

    def __str__(self):
        return f'Аукцион {self.id}'

    class Meta:
        verbose_name = "Аукцион"
        verbose_name_plural = "Аукционы"


class Auction_accept(models.Model):
    auction_id = models.OneToOneField(Auction, on_delete=models.PROTECT)
    accept = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    price_finish = models.IntegerField(default=0)
    commission = models.FloatField(default=0)
    end_bet = models.CharField(max_length=200)
    finish = models.BooleanField(default=False)

    def __str__(self):
        return f'Инфо по Аукциону {self.auction_id}'

    class Meta:
        verbose_name = "Инфо по Аукциону"
        verbose_name_plural = "Инфо по Аукционам"


@receiver(post_save, sender=Auction)
def save_auction(sender, instance, **kwargs):
    try:
        Auction_accept.objects.get(auction_id=instance)
        pass
    except:
        accept = Auction_accept(auction_id=instance, price_finish=instance.price, commission=instance.price * 0.5)
        accept.save()


@receiver(pre_save, sender=User)
def save_user(sender, instance, **kwargs):
    instance.is_staff = "1"


@receiver(post_save, sender=Claim_message)
def save_user(sender, instance, **kwargs):
    send_(-906481544, f'Сообщение от {instance.id_user} номер {instance.id} \n Текст: "{instance.massage_text}"')
