"""Factories for middleware tests."""
import factory
from factory.faker import faker
from wagtail.documents.models import Document
from wagtail.images.models import Image


def random_filename():
    """Use factory.faker to generate a random file name which includes an uppercase character."""
    filegen = faker.Faker()
    return filegen.random_uppercase_letter() + filegen.file_name()


class DocumentFactory(factory.django.DjangoModelFactory):
    """Factory for wagtail documents."""

    title = factory.Sequence(lambda n: f"document {n}")
    file = factory.django.FileField(filename=random_filename(), data=b'Test document')

    class Meta:
        """Define the Document model as meta class."""

        model = Document


class ImageFactory(factory.django.DjangoModelFactory):
    """Factory for wagtail images."""

    title = factory.Sequence(lambda n: f"image {n}")
    file = factory.django.ImageField(filename="MiXeDcAsE.jpg", data=b'Test image')

    class Meta:
        """Define the Image model as meta class."""

        model = Image
