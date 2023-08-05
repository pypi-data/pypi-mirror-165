"""

Product resource, it includes the class Resource and two request
classes to create and update the resource.

Author: Daniel Hernández - KEA

"""

import datetime as dt
from typing import ClassVar, Optional, cast, List

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from ..types.general import PendingSteps, Legal, CustomerAddress
from .base import Creatable, Queryable, Retrievable, Updatable, Deletable
import json
class OrganizationRequest(BaseModel):

    """
    This request must be filled to `create` an Organization.
    It contains all information necessary to create this resource.

    Attributes:
        name (str): Name of the organization

    """

    name: str

class OrganizationCerts(BaseModel):
    cer: str
    key: str
    password : str

class OrganizationUpdateRequest(BaseModel):
    """
    This request must be filled to `update` an Organization.
    It contains all information necessary to update this resource.

    Attributes:
        name (str): Name of the organization
        legal_name (str): Full name of the organization..
        tax_system (str): Tax regime of the customer.
        website (str): Website of the organization. Optional.
        support_email (str): Email of the organization. Optional.
        phone (str): Phone of the organization. Optional.
        address (CustomerAddress): Address object of the organization. Optional.

    """
    name: Optional[str]
    legal_name: Optional[str]
    tax_system: Optional[str]
    website: Optional[str]
    support_email: Optional[str]
    phone: Optional[str]
    address: Optional[CustomerAddress]

@dataclass
class Organizations(Creatable, Queryable, Retrievable, Updatable, Deletable):

    _resource: ClassVar = 'organizations'

    created_at: dt.datetime
    is_production_ready: bool
    pending_steps: Optional[List[PendingSteps]]
    legal: Optional[Legal]

    @classmethod
    def create(cls, data: OrganizationRequest) -> 'Organizations':
        """Create an Organization.

        Args:
            data: All the request data to create an Organization.

        Returns:
            Organization: The created Organization resource.

        """
        cleaned_data = data.dict(exclude_unset=True, exclude_none=True)
        return cast('Organizations', cls._create(**cleaned_data))

    @classmethod
    def update(cls, id: str, data: OrganizationUpdateRequest) -> 'Organizations':
        """Update an Organization.

        Args:
            id: ID of the Organization to be updated.
            data: Data to be updated.

        Returns:
            Organization: The udpated Organization resource.

        """
        cleaned_data = data.dict(exclude_unset=True, exclude_none=True)
        return cast('Organizations', cls._update(id=id+"/legal", **cleaned_data))

    @classmethod
    def get_test_key(cls, id: str, env: str):
        """Update an Organization.

        Args:
            id: ID of the Organization to be updated.
            data: Data to be updated.

        Returns:
            Organization: The udpated Organization resource.
        """

        retrieved_customer = Organizations.retrieve_keys(id=id,env=env)
        print(retrieved_customer)
        return retrieved_customer

    @classmethod
    def upload_certs(cls, id: str, data, files):
        """Update an Organization.

        Args:
            id: ID of the Organization to be updated.
            files: Files to be updated.

        Returns:
            Organization: The udpated Organization resource.
        """
        return cast('Organizations', cls._update_certs(id=id, files=files, data=data))
    
    @classmethod
    def upload_logo(cls, id: str, files) -> 'Organizations':
        """Update an Organization.

        Args:
            id: ID of the Organization to be updated.
            files: Files to be updated.

        Returns:
            Organization: The udpated Organization resource.
        """
        return cast('Organizations', cls._update_logo(id=id, files=files))