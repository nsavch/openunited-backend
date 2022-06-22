# Generated by Django 3.1 on 2022-06-18 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0014_auto_20220618_2252'),
        ('points_and_payments', '0002_auto_20220618_2252'),
        ('talent', '0046_personpreferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='bountydeliveryattempt',
            name='bounty_claim',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_attempt', to='matching.bountyclaim'),
        ),
        migrations.AddField(
            model_name='bountydeliveryattempt',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='talent.person'),
        ),
        migrations.AddField(
            model_name='bountydeliveryattachment',
            name='bounty_delivery_attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='matching.bountydeliveryattempt'),
        ),
    ]
