# Generated by Django 3.2.21 on 2023-09-14 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0005_alter_account_account_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=15, max_length=20, prefix='TRN', unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('description', models.CharField(blank=True, default='payment transaction', max_length=1000, null=True)),
                ('status', models.CharField(choices=[('failed', 'Failed'), ('completed', 'Completed'), ('pending', 'Pending'), ('processing', 'Processing')], default='pending', max_length=100)),
                ('transaction_type', models.CharField(choices=[('transfer', 'Transfer'), ('received', 'Received'), ('refund', 'Refund'), ('request', 'Request'), ('none', 'None')], default='none', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_transactions', to=settings.AUTH_USER_MODEL)),
                ('receiver_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_transactions_related', to='account.account')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_transactions', to=settings.AUTH_USER_MODEL)),
                ('sender_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_transactions_related', to='account.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]