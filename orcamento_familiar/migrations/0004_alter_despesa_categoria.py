# Generated by Django 4.0.6 on 2022-09-01 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento_familiar', '0003_remove_despesa_tipo_remove_receita_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='categoria',
            field=models.CharField(blank=True, choices=[('ALI', 'Alimentação'), ('SAU', 'Saúde'), ('MOR', 'Moradia'), ('TRA', 'Transporte'), ('EDU', 'Educação'), ('LAZ', 'Lazer'), ('IMP', 'Imprevistos'), ('OUT', 'Outras')], default='OUT', max_length=3),
        ),
    ]
