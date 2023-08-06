from __future__ import annotations
from typing import List
from pydantic import BaseModel
from etsy_apiv3.models.OfferingModel import Offering
from etsy_apiv3.models.PropertyValueModel import PropertyValue

class Product(BaseModel):
    product_id: int
    sku: str
    is_deleted: bool
    offerings: List[Offering]
    property_values: List[PropertyValue]