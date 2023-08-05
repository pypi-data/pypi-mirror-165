from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from UPS_SDK.models.Package import Package
from UPS_SDK.models.ShipTo import ShipTo
from UPS_SDK.models.Shipper import Shipper
from UPS_SDK.models.ReferenceNumberItem import ReferenceNumberItem
from UPS_SDK.models.Service import Service
from UPS_SDK.models.ShipmentWeight import ShipmentWeight

class Shipment(BaseModel):
    Shipper: Shipper
    ShipTo: ShipTo
    ShipmentWeight: Optional[ShipmentWeight]
    Service: Service
    ReferenceNumbers: Optional[List[ReferenceNumberItem]] = Field(None, alias="ReferenceNumber")
    ShipmentIdentificationNumber: str
    PickupDate: str
    ScheduledDeliveryDate: Optional[str]
    Package: Package
    
    @property
    def scheduled_delivery_date(self):
        date = None
        if self.Package.RescheduledDeliveryDate is not None:
            date = datetime.strptime(self.Package.RescheduledDeliveryDate, "%Y%m%d")
            
        elif self.ScheduledDeliveryDate is not None:
            date = datetime.strptime(self.ScheduledDeliveryDate, "%Y%m%d")
            
        return date
        