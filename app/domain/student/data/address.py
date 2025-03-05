from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


class AddressProps(BaseModel):
    suburb: Optional[str]
    city: Optional[str]
    zipcode: Optional[str]
    country: Optional[str]
    country_code: Optional[str]

    class Config:
        allow_mutation = True
        orm_mode = True


@dataclass
class AddressProp:
    props: AddressProps


@dataclass
class Address:
    props: AddressProps

    @staticmethod
    def create_address_response(props: AddressProps) -> AddressProp:
        if props is None:
            addr_props = AddressProps()
            return AddressProp(props=addr_props)

        addr_props = AddressProps(
            suburb=props.suburb,
            city=props.city,
            zipcode=props.zipcode,
            country_code=props.country_code,
        )
        return AddressProp(props=addr_props)
