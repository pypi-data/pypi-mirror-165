from __future__ import annotations
from pydantic import BaseModel, Field
from UPS_SDK.models.ActivityItem import ActivityItem
from UPS_SDK.models.Message import Message
from UPS_SDK.models.PackageWeight import PackageWeight
from UPS_SDK.models.ReferenceNumber import ReferenceNumber
from typing import List, Optional

class Package(BaseModel):
    TrackingNumber: str
    DeliveryIndicator: str
    RescheduledDeliveryDate: Optional[str]
    AllActivity: Optional[List[ActivityItem]] = Field(None, alias="Activity")

    Message: Optional[Message]
    PackageWeight: PackageWeight
    ReferenceNumber: Optional[ReferenceNumber]
    
    @property
    def get_US_activities(self) -> List[ActivityItem]:
        activities = []
        for activity in self.AllActivity:
            if activity.ActivityLocation is not None and activity.ActivityLocation.Address is not None and activity.ActivityLocation.Address.CountryCode == "US":
                activities.append(activity)
        return activities
    
    @property
    def is_delivered(self) -> bool:
        if "Delivered" in self.AllActivity[0].description:
            return True
        return False
    