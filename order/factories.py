from symtable import Class

import factory
from faker import Faker
from order.models import Order

fake = Faker()

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer_name = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.email())
    product_name = factory.LazyAttribute(lambda _: fake.word())
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=100))
    price = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=3, right_digits=2, positive=True))
    status = factory.Iterator(["pending", "processing", "shipped", "delivered"])
