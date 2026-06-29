from django.db import models
from django.contrib.auth.models import User


class ZaznamKnihaProvozu(models.Model):
    name = models.CharField('Název', max_length=100)
    version = models.CharField('Verze', max_length=50)
    author = models.CharField('Autor', max_length=100)
    location = models.CharField('Místo ( adresar )', max_length=100)
    command  = models.CharField('Příkaz', max_length=200)
    type_of_launch = models.CharField('Typ spuštění', max_length=50)
    trigger_frequency = models.CharField('Frekvence spuštění', max_length=50)
    description = models.TextField('Popis', null=True, blank=True)
    link_to_details= models.URLField('Odkaz na detaily', null=True, blank=True)
    status = models.CharField('Stav', max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added = models.DateTimeField('Datum publikace', auto_now_add=True)

    def __str__(self):
        return f"{self.name[:20]} – {self.version[:20]}"
        
    class Meta:
        verbose_name = 'zaznam kniha provozu'
        verbose_name_plural = 'zaznamy kniha provozu'
        ordering =  ['-added']
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('kniha_provozu:zaznam_detail', args=[str(self.id)])  
    
    
class HistorieKnihaProvozu(models.Model):
    zaznam_id = models.ForeignKey(ZaznamKnihaProvozu,on_delete=models.CASCADE,related_name='Id')
    date_run = models.DateTimeField('Datum spuštění', auto_now_add=True)
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
