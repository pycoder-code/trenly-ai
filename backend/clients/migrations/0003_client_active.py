from django.db import migrations, models


def mark_disconnected_inactive(apps, schema_editor):
    client = apps.get_model('clients', 'Client')
    client.objects.filter(status='disconnected').update(active=False)


def restore_status(apps, schema_editor):
    client = apps.get_model('clients', 'Client')
    client.objects.filter(active=False).update(status='disconnected')


class Migration(migrations.Migration):
    dependencies = [
        ('clients', '0002_alter_client_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='active',
            field=models.BooleanField(default=True, verbose_name='активен'),
        ),
        migrations.RunPython(mark_disconnected_inactive, restore_status),
        migrations.RemoveField(
            model_name='client',
            name='status',
        ),
    ]
