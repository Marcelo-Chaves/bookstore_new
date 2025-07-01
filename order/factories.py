from symtable import Class

import factory

from order.models import Order
from faker import Faker

fake = Faker()

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

        customer_name = factory.LazyAttribute(lambda _: fake.name())
        email = factory.lazy_attribute(lambda _: fake.email())
        product_name = factory.lazy_attribute(lambda _: fake.word())
        quantity = factory.lazy_attribute(lambda _: fake.random_int(min=1, max=100))
        price = factory.lazy_attribute(lambda _: fake.pydecimal(left_digits=3, right_digits=2, positive=True))
        status = factory.Iterator(["pending","processing","shipped","delivered"])

