from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'distributors',
            },
        ),
        migrations.CreateModel(
            name='Grape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'grapes',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.URLField(max_length=500)),
                ('alcohol_content', models.DecimalField(decimal_places=2, max_digits=7)),
                ('allergen', models.CharField(max_length=150)),
                ('highlight', models.TextField()),
                ('taste_summary', models.CharField(max_length=1000)),
                ('bold', models.DecimalField(decimal_places=2, max_digits=7)),
                ('sweet', models.DecimalField(decimal_places=2, max_digits=7)),
                ('acidic', models.DecimalField(decimal_places=2, max_digits=7)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.country')),
                ('distributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.distributor')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'regions',
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'styles',
            },
        ),
        migrations.CreateModel(
            name='Winery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'wineries',
            },
        ),
        migrations.CreateModel(
            name='WineType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'types',
            },
        ),
        migrations.CreateModel(
            name='Vintage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('feature', models.TextField(null=True)),
                ('discount_rate', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('edit_note', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('vin', models.TextField(null=True)),
                ('domaine', models.TextField(null=True)),
                ('vignoble', models.TextField(null=True)),
                ('stock', models.IntegerField(default=0)),
                ('average_score', models.FloatField(default=0)),
                ('total_rating', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vintages', to='product.product')),
            ],
            options={
                'db_table': 'vintages',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='account.account')),
                ('vintage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='product.vintage')),
            ],
            options={
                'db_table': 'ratings',
            },
        ),
        migrations.CreateModel(
            name='ProductGrape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.grape')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'db_table': 'products_grapes',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='grape',
            field=models.ManyToManyField(through='product.ProductGrape', to='product.Grape'),
        ),
        migrations.AddField(
            model_name='product',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.region'),
        ),
        migrations.AddField(
            model_name='product',
            name='style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.style'),
        ),
        migrations.AddField(
            model_name='product',
            name='wine_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.winetype'),
        ),
        migrations.AddField(
            model_name='product',
            name='winery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.winery'),
        ),
    ]
