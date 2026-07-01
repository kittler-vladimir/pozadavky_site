from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kniha_provozu', '0002_auto_20260630_0917'),
    ]

    operations = [
        migrations.RemoveField(model_name='zaznamknihaprovozu', name='den'),
        migrations.RemoveField(model_name='zaznamknihaprovozu', name='cas'),
        migrations.RemoveField(model_name='zaznamknihaprovozu', name='kde_server'),
        migrations.RemoveField(model_name='zaznamknihaprovozu', name='dir'),
        migrations.RemoveField(model_name='zaznamknihaprovozu', name='popis'),
        migrations.RemoveField(model_name='zaznamknihaprovozu', name='text'),
        migrations.RemoveField(model_name='zaznamknihaprovozu', name='kdo'),
        migrations.RemoveField(model_name='zaznamknihaprovozu', name='poznamka'),
        migrations.RemoveField(model_name='zaznamknihaprovozu', name='created_by'),

        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='name',
            field=models.CharField(default='', max_length=200, verbose_name='Název'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='version',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Verze'),
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='author',
            field=models.CharField(default='', max_length=150, verbose_name='Autor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='location',
            field=models.CharField(default='', max_length=200, verbose_name='Místo (adresář)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='command',
            field=models.TextField(default='', verbose_name='Příkaz'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='type_of_launch',
            field=models.CharField(
                choices=[
                    ('Manuálně', 'Manuálně'),
                    ('Naplánovaně (cron)', 'Naplánovaně (cron)'),
                    ('Při události', 'Při události'),
                ],
                default='Manuálně',
                max_length=50,
                verbose_name='Typ spuštění',
            ),
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='trigger_frequency',
            field=models.CharField(
                choices=[
                    ('Jednorázově', 'Jednorázově'),
                    ('Denně', 'Denně'),
                    ('Týdně', 'Týdně'),
                    ('Měsíčně', 'Měsíčně'),
                    ('Ročně', 'Ročně'),
                    ('Jinak', 'Jinak'),
                ],
                default='Jednorázově',
                max_length=50,
                verbose_name='Frekvence spuštění',
            ),
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Popis'),
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='link_to_details',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Odkaz na detaily'),
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='status',
            field=models.CharField(
                choices=[
                    ('Aktivní', 'Aktivní'),
                    ('Neaktivní', 'Neaktivní'),
                    ('Ukončené', 'Ukončené'),
                    ('Zastavené', 'Zastavené'),
                    ('Zastaralé', 'Zastaralé'),
                ],
                default='Aktivní',
                max_length=50,
                verbose_name='Stav',
            ),
        ),
        migrations.AddField(
            model_name='zaznamknihaprovozu',
            name='created_by',
            field=models.CharField(default='', editable=False, max_length=150, verbose_name='Vytvořil'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='zaznamknihaprovozu',
            name='added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Datum publikace'),
        ),
        migrations.AlterModelOptions(
            name='zaznamknihaprovozu',
            options={
                'ordering': ['-added'],
                'verbose_name': 'záznam kniha provozu',
                'verbose_name_plural': 'záznamy kniha provozu',
            },
        ),
    ]
