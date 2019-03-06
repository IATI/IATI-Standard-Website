import factory
from factory.faker import faker
from wagtail.documents.models import Document
from wagtail.images.models import Image

def random_filename():
	filegen = faker.Faker()
	return filegen.random_uppercase_letter() + filegen.file_name()

class DocumentFactory(factory.django.DjangoModelFactory):
	title = factory.Sequence(lambda n: f"document {n}")
	file = factory.django.FileField(filename=random_filename(), data=b'Test document')

	class Meta:
		model = Document

class ImageFactory(factory.django.DjangoModelFactory):
	title = factory.Sequence(lambda n: f"image {n}")
	file = factory.django.ImageField(filename="MiXeDcAsE.jpg", data=b'Test image')

	class Meta:
		model = Image
