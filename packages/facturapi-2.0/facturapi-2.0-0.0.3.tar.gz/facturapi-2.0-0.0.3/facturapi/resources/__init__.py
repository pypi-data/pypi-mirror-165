__all__ = [
    'Customer',
    'Invoice',
    'Product',
    'Organizations'
]

from .customers import Customer
from .invoices import Invoice
from .products import Product
from .organizations import Organizations
from .resources import RESOURCES

resource_classes = [
    Customer,
    Invoice,
    Product,
    Organizations
]
for resource_cls in resource_classes:
    RESOURCES[resource_cls._resource] = resource_cls  # type: ignore
