# Generated by Django 4.0.6 on 2022-09-01 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento_familiar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Despesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=10, max_digits=20)),
                ('data', models.DateField()),
                ('tipo', models.CharField(choices=[('D', 'Despesa'), ('R', 'Receita')], default='D', max_length=1)),
                ('categoria', models.CharField(choices=[('ALI', 'Alimentação'), ('SAU', 'Saúde'), ('MOR', 'Moradia'), ('TRA', 'Transporte'), ('EDU', 'Educação'), ('LAZ', 'Lazer'), ('IMP', 'Imprevistos'), ('OUT', 'Outras')], default='OUT', max_length=3)),
            ],
            options={
                'verbose_name': 'Despesa',
                'verbose_name_plural': 'Despesas',
            },
        ),
        migrations.CreateModel(
            name='Receita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=10, max_digits=20)),
                ('data', models.DateField()),
                ('tipo', models.CharField(choices=[('D', 'Despesa'), ('R', 'Receita')], default='D', max_length=1)),
            ],
            options={
                'verbose_name': 'Receita',
                'verbose_name_plural': 'Receitas',
            },
        ),
        migrations.DeleteModel(
            name='Transacao',
        ),
    ]