from django.views import generic
from ads.models import AdModel
from datetime import datetime


class AdView(generic.ListView):
    model = AdModel
    template_name = 'Ads/main.html'
    context_object_name = 'ads'

    def get_queryset(self):
        """Функция находящая последнюю запись с горячей ценой"""
        return AdModel.objects.filter(disappear_at__gte=datetime.now(), hot_price=True)[0:1]

    def get_context_data(self, *, object_list=None, **kwargs):
        """Функция находящая записи без горячей цены"""
        context = super().get_context_data(**kwargs)
        context['ads_without_a_hot_price'] = AdModel.objects.filter(disappear_at__gte=datetime.now(), hot_price=False)
        return context

