# Generated by Django 3.2.21 on 2023-09-22 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('failed', 'Failed'), ('completed', 'Completed'), ('pending', 'Pending'), ('processing', 'Processing'), ('requested', 'Requested'), ('request_sent', 'request_sent'), ('request_settled', 'request settled'), ('request_processing', 'Request Processing')], default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('transfer', 'Transfer'), ('received', 'Received'), ('refund', 'Refund'), ('request', 'Payment Request'), ('none', 'None')], default='none', max_length=100),
        ),
    ]
