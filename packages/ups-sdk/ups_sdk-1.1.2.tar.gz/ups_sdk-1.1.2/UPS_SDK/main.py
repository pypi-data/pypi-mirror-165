import asyncio
from time import perf_counter
import requests, urllib3, xmltodict, json
from UPS_SDK.models.TrackError import TrackError
from UPS_SDK.models.TrackResponse import TrackResponse
from UPS_SDK.models.TrackType import TrackType
from UPS_SDK.utils.xml_request_creator import create_xml_data
urllib3.disable_warnings()
from aiohttp import ClientSession

    
class UPSApi:
    def __init__(self, access_license_number: str, user_id: str, password: str):
        """
        Create A Ups SDK

        Args:
            access_license_number (str): API Access License Number
            user_id (str): API User ID
            password (str): API Password
        """
        
        self.access_license_number = access_license_number
        self.user_id = user_id
        self.password = password
        self.host = 'https://onlinetools.ups.com/ups.app/xml/Track'

    @staticmethod
    def __create_response(text: str) -> TrackResponse:
        xpars = xmltodict.parse(text, dict_constructor=dict)
        track_response: dict = json.loads(json.dumps(xpars))["TrackResponse"]
        
        if "Error" in track_response["Response"].keys():
            raise TrackError(**track_response["Response"]["Error"])
        
        response = TrackResponse(**track_response)
        
        return response
    
    def get_package(self, reference_number_or_tracking_number: str, track_type: TrackType = TrackType.ByTrackingNumber):
        """
        Get Tracking Information By ReferenceNumber Or TrackingNumber

        Args:
            reference_number_or_tracking_number (str): ReferenceNumber Or TrackingNumber
            track_type (TrackType): TrackType For Find

        Returns:
            TrackResponse: TrackResponse Object Or Raise TrackError
        """
        xml_data = create_xml_data(
            self.access_license_number, self.user_id, self.password,
            track_type, reference_number_or_tracking_number
        )
        
        response = requests.post(self.host, xml_data, verify=False)
        
        return self.__create_response(response.text)

    
    async def async_get_package(self, session: ClientSession, reference_number_or_tracking_number: str, track_type: TrackType = TrackType.ByTrackingNumber):
        xml_data = create_xml_data(
            self.access_license_number, self.user_id, self.password,
            track_type, reference_number_or_tracking_number
        )
        
        response = await session.post(self.host, data=xml_data)
        text = await response.text()
        
        return self.__create_response(text)
    