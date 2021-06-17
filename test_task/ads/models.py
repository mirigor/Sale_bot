from django.db import models


class AdModel(models.Model):
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-disappear_at']

    name = models.CharField(max_length=200, verbose_name='Название')
    price = models.FloatField(verbose_name='Цена', null=True)
    hot_price = models.BooleanField(verbose_name='Горячая цена ?', null=True)
    disappear_at = models.TimeField(auto_now_add=True, verbose_name='Время исчезновения объявления')

    def __str__(self):
        return self.name
