from random import randint

from django.utils.text import slugify


def convert_title_to_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    if instance.__class__.objects.filter(slug=slug).exists():
        slug = slugify(instance.title) + str(randint(100_000, 999_999))
        convert_title_to_slug(instance, new_slug=slug)

    return slug
