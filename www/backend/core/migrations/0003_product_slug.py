# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.template.defaultfilters import slugify
from django.apps import apps
from django.db import migrations, models


def _get_unique_slug(Product, p):
    slug = slugify(p.name[:40])
    unique_slug = slug
    num = 1
    while Product.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug


def populate_product_slug(*args, **kwargs):
    Product = apps.get_model('core', 'Product')
    for p in Product.objects.all():
        p.slug = _get_unique_slug(Product, p)
        p.save()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_insert_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=uuid.uuid4()),
            preserve_default=False,
        ),
        migrations.RunPython(populate_product_slug),
        migrations.AlterField(model_name='product',
                              name='slug',
                              field=models.SlugField(unique=True),
                              preserve_default=False)
    ]
