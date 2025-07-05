from fastapi import APIRouter, Depends, HTTPException, status 
from typing import Optional
from bson import ObjectId
from datetime import date, time
from app import crud, schemas
from app.database import get_database  # should return AsyncIOMotorDatabase instance
from app.schemas import ShipmentStatusUpdate

router = APIRouter(prefix="/api/v1/shipments", tags=["Shipments"])


@router.post("/", response_model=schemas.ShipmentOut, status_code=status.HTTP_201_CREATED)
async def create_shipment(
    shipment: schemas.ShipmentCreate,
    db=Depends(get_database)
):
    """
    Create a new shipment document in MongoDB.
    """
    try:
        new_shipment = await crud.create_shipment(db, shipment)
        return new_shipment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{shipment_id}", response_model=schemas.ShipmentOut)
async def get_shipment(
    shipment_id: str,
    db=Depends(get_database)
):
    """
    Retrieve a shipment by its MongoDB ObjectId.
    """
    if not ObjectId.is_valid(shipment_id):
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")

    shipment = await crud.get_shipment_by_id(db, shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.get("/tracking/{tracking_number}", response_model=schemas.ShipmentOut)
async def get_shipment_by_tracking(
    tracking_number: str,
    db=Depends(get_database)
):
    """
    Retrieve a shipment by its tracking number.
    """
    shipment = await crud.get_shipment_by_tracking_number(db, tracking_number)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.put("/tracking/{tracking_number}", response_model=schemas.ShipmentOut)
async def update_shipment_status(
    tracking_number: str,
    status_update: schemas.ShipmentStatusUpdate,
    db=Depends(get_database)
):
    """
    Update the shipment status and related fields.
    Only fields provided in the request will be updated.
    """
    shipment = await crud.get_shipment_by_tracking_number(db, tracking_number)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    update_data = {}

    # Convert date/time and enum fields to strings for MongoDB
    for field in [
        "status",
        "latest_status_date",
        "latest_status_time",
        "current_location",
        "next_transit_port",
        "current_location_coords",
        "destination_coords",
    ]:
        value = getattr(status_update, field, None)
        if value is not None:
            if isinstance(value, (date, time)):
                value = value.isoformat()
            elif hasattr(value, "dict"):  # For nested Pydantic models like GeoLocation
                value = value.dict()
            elif hasattr(value, "value"):  # For enums, get the underlying value
                value = value.value
            update_data[field] = value

    if update_data:
        result = await db["shipments"].update_one(
            {"tracking_number": tracking_number},
            {"$set": update_data},
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to update shipment")

    # Fetch and return the updated shipment
    updated_shipment = await crud.get_shipment_by_tracking_number(db, tracking_number)
    return updated_shipment


@router.delete("/tracking/{tracking_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment(
    tracking_number: str,
    db=Depends(get_database)
):
    """
    Delete a shipment by tracking number.
    """
    success = await crud.delete_shipment(db, tracking_number)
    if not success:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return None
