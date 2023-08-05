"""

Product resource, it includes the class Resource and two request
classes to create and update the resource.

Author: Daniel Hernández - KEA

"""

import datetime as dt
from typing import ClassVar, Optional, cast, List

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from ..types.general import Taxes, LocalTaxes
from .base import Creatable, Queryable, Retrievable, Updatable, Deletable

class ProductRequest(BaseModel):

    """
    This request must be filled to `create` a Product.
    It contains all information necessary to create this resource.

    Attributes:
        description (str): Description of the product
        product_key (str): Key of the product
        price (float): Price unit of the product
        tax_included (bool): Flag if price includes taxes.
        taxability (str): Code that represents if the product is subject to taxes or not.
        taxes (List[Taxes]): List of taxes that should be applied to this product.
        local_taxes(List[LocalTaxes]): List of local taxes that should be applied to this product.
        unit_key (str): Unit of measure key
        unit_name (str): Represents the unit of measure of your product
        sku (str): Identifier for internal use designated by the company

    """

    description: str
    product_key: str 
    price: float
    tax_included: Optional[bool]
    taxability: Optional[str]
    taxes: Optional[List[Taxes]]
    local_taxes: Optional[List[LocalTaxes]]
    unit_key: Optional[str]
    unit_name: Optional[str]
    sku: Optional[str]

class ProductUpdateRequest(BaseModel):
    """
    This request must be filled to `update` a Product.
    It contains all information necessary to update this resource.

    Attributes:
        description (str): Description of the product
        product_key (str): Key of the product
        price (float): Price unit of the product
        tax_included (bool): Flag if price includes taxes.
        taxability (str): Code that represents if the product is subject to taxes or not.
        taxes (List[Taxes]): List of taxes that should be applied to this product.
        local_taxes(List[LocalTaxes]): List of local taxes that should be applied to this product.
        unit_key (str): Unit of measure key
        unit_name (str): Represents the unit of measure of your product
        sku (str): Identifier for internal use designated by the company

    """

    description: Optional[str]
    product_key: Optional[str]
    price: Optional[float]
    tax_included: Optional[bool]
    taxability: Optional[str]
    taxes: Optional[List[Taxes]]
    local_taxes: Optional[List[LocalTaxes]]
    unit_key: Optional[str]
    unit_name: Optional[str]
    sku: Optional[str]

@dataclass
class Product(Creatable, Queryable, Retrievable, Updatable, Deletable):

    _resource: ClassVar = 'products'

    created_at: dt.datetime
    livemode: bool
    description: str
    product_key: str 
    price: float
    tax_included: Optional[bool]
    taxability: Optional[str]
    taxes: Optional[List[Taxes]]
    local_taxes: Optional[List[LocalTaxes]]
    unit_key: Optional[str]
    unit_name: Optional[str]
    sku: Optional[str]

    @classmethod
    def create(cls, data: ProductRequest) -> 'Product':
        """Create a product.

        Args:
            data: All the request data to create a product.

        Returns:
            Product: The created product resource.

        """
        cleaned_data = data.dict(exclude_unset=True, exclude_none=True)
        return cast('Product', cls._create(**cleaned_data))

    @classmethod
    def update(cls, id: str, data: ProductUpdateRequest) -> 'Product':
        """Update a customer.

        Args:
            id: ID of the customer to be updated.
            data: Data to be updated.

        Returns:
            Product: The udpated product resource.

        """
        cleaned_data = data.dict(exclude_unset=True, exclude_none=True)
        return cast('Product', cls._update(id=id, **cleaned_data))