from django.db import migrations


class Migration(migrations.Migration):
    # Fixes casing mismatch from 0001_initial ('requirement_type' vs models.py's
    # 'Requirement_type') that made makemigrations regenerate a no-op AlterField every run.
    # Two-step rename works around a Django RenameModel bug: a case-only rename collides
    # with its own lowercase state key (old_name.lower() == new_name.lower()) and raises
    # KeyError in state_forwards, so we go through a differently-cased intermediate name.

    dependencies = [
        ('pozadavky', '0043_auto_20260629_1255'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='requirement_type',
            new_name='requirement_type_tmp',
        ),
        migrations.RenameModel(
            old_name='requirement_type_tmp',
            new_name='Requirement_type',
        ),
    ]
