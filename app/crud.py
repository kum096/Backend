from typing import Optional, List, Dict
from bson import ObjectId
from . import schemas


def obj_id_to_str(doc: Optional[dict]) -> Optional[dict]:
    """
    Convert MongoDB's ObjectId to a string and rename `_id` to `id`.
    """
    if doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


async def create_shipment(db, shipment_data: schemas.ShipmentCreate) -> dict:
    """
    Insert a new shipment document into the database.
    """
    shipment_dict = shipment_data.dict()
    result = await db["shipments"].insert_one(shipment_dict)
    new_shipment = await db["shipments"].find_one({"_id": result.inserted_id})
    return obj_id_to_str(new_shipment)


async def get_shipment_by_tracking_number(db, tracking_number: str) -> Optional[dict]:
    """
    Find a shipment by its tracking number.
    """
    shipment = await db["shipments"].find_one({"tracking_number": tracking_number})
    return obj_id_to_str(shipment)


async def get_shipment_by_id(db, shipment_id: str) -> Optional[dict]:
    """
    Find a shipment by its MongoDB _id.
    """
    if not ObjectId.is_valid(shipment_id):
        return None
    shipment = await db["shipments"].find_one({"_id": ObjectId(shipment_id)})
    return obj_id_to_str(shipment)


async def update_shipment(db, tracking_number: str, update_data: Dict) -> Optional[dict]:
    """
    Update fields of a shipment document by tracking number.
    """
    if not update_data:
        return None

    result = await db["shipments"].update_one(
        {"tracking_number": tracking_number},
        {"$set": update_data}
    )

    if result.modified_count == 1:
        return await get_shipment_by_tracking_number(db, tracking_number)

    return None


async def get_all_shipments(db, skip: int = 0, limit: int = 1000) -> List[dict]:
    """
    Retrieve all shipment documents with optional pagination.
    """
    cursor = db["shipments"].find().skip(skip).limit(limit)
    shipments = []
    async for shipment in cursor:
        shipments.append(obj_id_to_str(shipment))
    return shipments


async def delete_shipment(db, tracking_number: str) -> bool:
    """
    Delete a shipment by its tracking number.
    """
    result = await db["shipments"].delete_one({"tracking_number": tracking_number})
    return result.deleted_count == 1
