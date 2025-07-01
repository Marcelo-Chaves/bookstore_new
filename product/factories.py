import factory

from product.models import Category, Product
from faker import Faker

fake = Faker

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

        name = factory.lazy_attribute(lambda _: fake.word())

class ProductFactory(factory.django.DjangoModelFactory):
     class Meta:
         model = Product

         name = factory.lazy_attribute(lambda _: fake.word())
         description = factory.lazy_attribute(lambda _: fake.sentence())
         price = factory.lazy_attribute(lambda _: fake.pydecimal(left_digits=3, right_digits=2, positive=True) )
         stock = factory.lazy_attribute(lambda _: fake.random_int(min=0, max=1000))
         is_active = True
         category = factory.SubFactory(CategoryFactory)