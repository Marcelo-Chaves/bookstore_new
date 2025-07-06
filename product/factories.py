import factory
from faker import Faker
from product.models import Category, Product

fake = Faker()



class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: fake.word())

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.sentence())
    price = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=3, right_digits=2, positive=True))
    stock = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=1000))
    is_active = True
    category = factory.SubFactory(CategoryFactory)
