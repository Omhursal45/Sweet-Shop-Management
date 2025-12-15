# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sweet',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sweet',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='sweets/'),
        ),
        migrations.AddField(
            model_name='sweet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, default=None),
        ),
        migrations.AddField(
            model_name='sweet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, default=None),
        ),
        migrations.AlterField(
            model_name='sweet',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name='sweet',
            options={'ordering': ['-created_at']},
        ),
    ]

