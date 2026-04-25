# Generated manually for HeroSlide model

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_sitesettings_accent_color_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fr', models.CharField(max_length=100, verbose_name='Title (French)')),
                ('title_ar', models.CharField(blank=True, max_length=100, verbose_name='Title (Arabic)')),
                ('description_fr', models.TextField(max_length=300, verbose_name='Description (French)')),
                ('description_ar', models.TextField(blank=True, max_length=300, verbose_name='Description (Arabic)')),
                ('icon', models.CharField(choices=[('car', 'Car'), ('shopping-bag', 'Shopping Bag'), ('building', 'Building'), ('briefcase', 'Briefcase'), ('code', 'Code'), ('globe', 'Globe'), ('smartphone', 'Smartphone'), ('zap', 'Zap')], default='code', max_length=20, verbose_name='Icon')),
                ('color_theme', models.CharField(choices=[('blue', 'Blue (Rental)'), ('purple', 'Purple (E-commerce)'), ('emerald', 'Emerald (Business)'), ('orange', 'Orange (Portfolio)'), ('red', 'Red'), ('pink', 'Pink'), ('cyan', 'Cyan'), ('indigo', 'Indigo')], default='blue', max_length=20, verbose_name='Color Theme')),
                ('link', models.URLField(blank=True, help_text='Optional link for the slide', verbose_name='Link')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Hero Slide',
                'verbose_name_plural': 'Hero Slides',
                'ordering': ['order', 'created_at'],
            },
        ),
    ]
