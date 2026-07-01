from django.db import models
from django.contrib.auth.models import User


TYPE_OF_LAUNCH_CHOICES = (
    ('Manuálně', 'Manuálně'),
    ('Naplánovaně (cron)', 'Naplánovaně (cron)'),
    ('Při události', 'Při události'),
)

TRIGGER_FREQUENCY_CHOICES = (
    ('Jednorázově', 'Jednorázově'),
    ('Denně', 'Denně'),
    ('Týdně', 'Týdně'),
    ('Měsíčně', 'Měsíčně'),
    ('Ročně', 'Ročně'),
    ('Jinak', 'Jinak'),
)

STATUS_CHOICES = (
    ('Aktivní', 'Aktivní'),
    ('Neaktivní', 'Neaktivní'),
    ('Ukončené', 'Ukončené'),
    ('Zastavené', 'Zastavené'),
    ('Zastaralé', 'Zastaralé'),
)


class ZaznamKnihaProvozu(models.Model):
    name = models.CharField('Název', max_length=200)
    version = models.CharField('Verze', max_length=50, blank=True, null=True)
    author = models.CharField('Autor', max_length=150)
    location = models.CharField('Místo (adresář)', max_length=200)
    command = models.TextField('Příkaz')
    launched_at = models.DateTimeField('Spuštěno', blank=True, null=True)
    type_of_launch = models.CharField(
        'Typ spuštění', max_length=50, choices=TYPE_OF_LAUNCH_CHOICES, default='Manuálně'
    )
    trigger_frequency = models.CharField(
        'Frekvence spuštění', max_length=50, choices=TRIGGER_FREQUENCY_CHOICES, default='Jednorázově'
    )
    description = models.TextField('Popis', blank=True, null=True)
    link_to_details = models.URLField('Odkaz na detaily', max_length=500, blank=True, null=True)
    status = models.CharField(
        'Stav', max_length=50, choices=STATUS_CHOICES, default='Aktivní'
    )

    created_by = models.CharField('Vytvořil', max_length=150, editable=False)
    added = models.DateTimeField('Datum publikace', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'záznam kniha provozu'
        verbose_name_plural = 'záznamy kniha provozu'
        ordering = ['-added']

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
