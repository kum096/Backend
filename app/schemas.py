from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time
from enum import Enum


class ShipmentStatus(str, Enum):
    pending = "pending"
    in_transit = "in_transit"
    delivered = "delivered"
    canceled = "canceled"


class ShippingMode(str, Enum):
    air = "air"
    sea = "sea"
    land = "land"


class GeoLocation(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ShipmentBase(BaseModel):
    tracking_number: str
    sender_name: str
    sender_number: Optional[str] = None
    sender_email: Optional[EmailStr] = None
    sender_address: Optional[str] = None

    receiver_name: str
    receiver_number: Optional[str] = None
    receiver_email: Optional[EmailStr] = None
    receiver_address: Optional[str] = None

    registration_date: Optional[date] = None
    product_description: Optional[str] = None
    quantity: Optional[str] = None
    weight: Optional[str] = None

    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None
    shipping_mode: Optional[ShippingMode] = None
    voyage: Optional[str] = None

    departure_date: Optional[date] = None
    expected_arrival_date: Optional[date] = None
    carrier: Optional[str] = None
    vessel: Optional[str] = None

    latest_status_date: Optional[date] = None
    latest_status_time: Optional[time] = None
    current_location: Optional[str] = None
    current_location_coords: Optional[GeoLocation] = None

    next_transit_port: Optional[str] = None
    destination_coords: Optional[GeoLocation] = None

    status: Optional[ShipmentStatus] = None


class ShipmentCreate(ShipmentBase):
    """For creating a new shipment (no additional fields required)."""
    pass


class ShipmentStatusUpdate(BaseModel):
    """
    Used to update tracking/status fields.
    Only fields provided will be updated.
    """
    status: Optional[ShipmentStatus] = None
    latest_status_date: Optional[date] = None
    latest_status_time: Optional[time] = None
    current_location: Optional[str] = None
    current_location_coords: Optional[GeoLocation] = None
    next_transit_port: Optional[str] = None
    destination_coords: Optional[GeoLocation] = None


class ShipmentOut(ShipmentBase):
    """
    Response schema including MongoDB ID.
    """
    id: str


    class Config:
       orm_mode = True

    class Config:
         arbitrary_types_allowed = True
    json_encoders = {
        date: lambda v: v.isoformat(),
        time: lambda v: v.isoformat(),
    }
    
