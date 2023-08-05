from typing import List, Optional
import datetime as dt

from pydantic import BaseModel

from .validators import sanitize_dict
from .enums import Steps


class CustomerAddress(BaseModel):
    """Address of a customer.

    Attributes:
        street (str): Street.
        exterior (str): Exterior place number.
        interior (str): Interior place number.
        neighborhood (str): 'Colonia'.
        city (str): City.
        municipality (str): 'Municipio or Alcaldía'.
        state (str): State of the address.
        zip (str): Postal code.
        country (str): Country.

    """

    street: Optional[str]
    exterior: Optional[str]
    interior: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    municipality: Optional[str]
    zip: Optional[str]
    state: Optional[str]
    country: Optional[str]

class Taxes(BaseModel):
    """Taxes basic info."""
    type: Optional[str]
    rate: Optional[float]
    factor : Optional[str]
    withholding: Optional[bool]

class LocalTaxes(BaseModel):
    """Local taxes info"""
    rate: Optional[float]
    type: Optional[str]
    withholding: Optional[bool]


class CustomerBasicInfo(BaseModel):
    """Customer's basic info"""

    id: str
    legal_name: str
    tax_id: str
    tax_system: str


class ItemPart(BaseModel):
    """Defines a part of an invoice item."""

    description: str
    product_key: str
    quantity: Optional[int] = 1
    sku: Optional[str]
    unit_price: Optional[float]
    customs_keys: Optional[List[str]]


class Namespace(BaseModel):
    """Namespace for spceial XML namespaces for an invoice."""

    prefix: Optional[str]
    uri: Optional[str]
    schema_location: Optional[str]


class ProductBasicInfo(BaseModel):
    """Product's basic info."""

    id: str
    unit_name: str
    description: str

class InvoiceDocuments(BaseModel):
    relationship : str
    documents : List

class InvoiceStamp(BaseModel):
    signature : str
    date : dt.datetime
    sat_cert_number: str
    sat_signature: str

class PendingSteps(BaseModel):
    type: Optional[Steps]
    description : str

class Legal(BaseModel):
    name: str
    legal_name: str
    tax_system: Optional[str]
    website: Optional[str]
    phone: Optional[str]

class SanitizedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sanitize_dict(self)




