from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='vintage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.vintage'),
        ),
    ]
