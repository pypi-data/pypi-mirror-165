__all__ = [
    '__version__',
    'Customer',
    'Invoice',
    'Product',
    'Organizations'
    'configure',
]

from .http import client
from .resources import Customer, Invoice, Product, Organizations
from .version import __version__

configure = client.configure
