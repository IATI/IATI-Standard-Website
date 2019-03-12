"""Factories for middleware tests."""
import factory
from factory.faker import faker
from wagtail.documents.models import Document


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
