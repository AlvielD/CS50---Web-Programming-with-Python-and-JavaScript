# Generated by Django 4.2.3 on 2023-08-27 17:16

import auctions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_auctionlisting_comment_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionlisting",
            name="author",
            field=models.ForeignKey(
                default=auctions.models.get_default_user,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
