from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_auto_20230506_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='nmapscandb',
            name='is_vulners',
            field=models.BooleanField(default=False),
        ),
    ]
