# Generated by Django 4.0.3 on 2022-03-23 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weddingapi', '0008_exampleimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendortype',
            name='image',
            field=models.ImageField(default=None, upload_to='vendortypes'),
            preserve_default=False,
        ),
    ]
