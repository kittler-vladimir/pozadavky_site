from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.utils.safestring import mark_safe
#from smart_selects.db_fields import ChainedForeignKey
from django_middleware_global_request import get_request


# ------------------------------
# Výběr kategorií úkolů
# ------------------------------
task_category_choices = (
    (0, 'Neuvedeno'),
    (1, 'Trvalý'),
    (2, 'Ginis - (e-mail)'),
    (3, 'Z porady'),
    (4, 'Vlastní'),
    (5, 'Pracovní skupina C227'),
    (6, 'Hlavní projektový tým C227'),
    (7, 'Řídící výbor C227'),
)


# ------------------------------
# Stav úkolu
# ------------------------------
class Work_status(models.Model):
    status_text = models.CharField('Text', max_length=20, unique=True)

    def __str__(self):
        return self.status_text

    class Meta:
        ordering = ['status_text']
        verbose_name = 'stav práce'
        verbose_name_plural = 'stavy prací'


# ------------------------------
# Typ požadavku
# ------------------------------
class Requirement_type(models.Model):
    requirement_type_text = models.CharField('Text', max_length=30, unique=True)

    def __str__(self):
        return self.requirement_type_text

    class Meta:
        ordering = ['requirement_type_text']
        verbose_name = 'typ požadavku'
        verbose_name_plural = 'typy požadavků'


# ------------------------------
# Hlavní model Úkolu
# ------------------------------
class Requirement(models.Model):
    requirement = models.CharField('Úkol', max_length=100)
    cislo_jednaci = models.CharField('Č. j.', max_length=25, null=True, blank=True)

    author = models.ForeignKey(
        User,
        verbose_name='Zadal',
        editable=False,
        on_delete=models.PROTECT,
        related_name='requirements_created'
    )

    status = models.ForeignKey(
        Work_status,
        verbose_name='Stav požadavku',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    category = models.PositiveSmallIntegerField(
        'Kategorie úkolu',
        choices=task_category_choices
    )

    description = models.TextField('Popis', null=True, blank=True)

    requirement_type = models.ForeignKey(
        Requirement_type,
        verbose_name='Typ požadavku',
        on_delete=models.PROTECT
    )

    group_owner = models.ForeignKey(
        Group,
        verbose_name='Oddělení',
        on_delete=models.CASCADE
    )

    owner = models.ForeignKey(
        User,
        verbose_name="Vlastník",
        limit_choices_to={'is_active': True},
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='requirements_owned'
    )

    added = models.DateTimeField('Datum publikace', auto_now_add=True)
    deadline = models.DateField('Termín', null=True, blank=True)
    done = models.DateField('Ukončeno', null=True, blank=True)

    # --------------------------
    # Automatická logika při uložení
    # --------------------------
    def save(self, *args, **kwargs):
        # Automaticky nastav stav podle "done"
        if self.done:
            status, _ = Work_status.objects.get_or_create(status_text__iexact="Splněno", defaults={"status_text": "Splněno"})
        else:
            status, _ = Work_status.objects.get_or_create(status_text__iexact="Rozpracováno", defaults={"status_text": "Rozpracováno"})
        self.status = status

        super().save(*args, **kwargs)

    def __str__(self):
        return self.requirement

    class Meta:
        verbose_name = 'úkol'
        verbose_name_plural = 'úkoly'
        ordering =  ['-id']  # nebo  ['-added']

    @property
    def safe_description(self):
        return mark_safe(self.description or "")
