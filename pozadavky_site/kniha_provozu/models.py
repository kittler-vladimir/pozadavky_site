from django.db import models
from django.contrib.auth.models import User


class ZaznamKnihaProvozu(models.Model):
    den = models.DateField('Den')
    cas = models.TimeField('Čas')
    kde_server = models.CharField('Kde (server)', max_length=100)
    dir = models.CharField('Dir', max_length=200, blank=True, null=True)
    popis = models.CharField(
        'Popis (bližší specifikace/doména/sql)', max_length=255, blank=True, null=True
    )
    text = models.CharField('Text', max_length=150, blank=True, null=True)
    kdo = models.CharField('Kdo', max_length=100)
    poznamka = models.TextField('Poznámka', blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added = models.DateTimeField('Datum vytvoření záznamu', auto_now_add=True)

    def __str__(self):
        return f"{self.den} {self.cas} — {self.kde_server}"

    class Meta:
        verbose_name = 'záznam kniha provozu'
        verbose_name_plural = 'záznamy kniha provozu'
        ordering = ['-den', '-cas']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('kniha_provozu:zaznam_detail', args=[str(self.id)])


class HistorieKnihaProvozu(models.Model):
    zaznam_id = models.ForeignKey(ZaznamKnihaProvozu, on_delete=models.CASCADE, related_name='Id')
    date_run = models.DateTimeField('Datum změny', auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field_name = models.CharField('Pole', max_length=100)
    old_value = models.TextField('Původní hodnota', blank=True, null=True)
    new_value = models.TextField('Nová hodnota', blank=True, null=True)
    note = models.CharField('Poznámka', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Historie (kniha provozu)"
        verbose_name_plural = "Historie (kniha provozu)"
        ordering = ['-date_run']

    def __str__(self):
        return f"Zápis {self.field_name} dne {self.date_run.strftime('%Y-%m-%d %H:%M:%S')}"
