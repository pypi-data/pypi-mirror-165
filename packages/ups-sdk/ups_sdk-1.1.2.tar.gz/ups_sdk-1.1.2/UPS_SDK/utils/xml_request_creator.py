__XML_REQUEST = """
<?xml version='1.0' encoding='utf8'?>
    <AccessRequest>
        <AccessLicenseNumber>{access_license_number}</AccessLicenseNumber>
        <UserId>{user_id}</UserId>
        <Password>{password}</Password>
    </AccessRequest>
<?xml version='1.0' encoding='utf8'?>
    <TrackRequest>
        <Request>
            <TransactionReference>
                <CustomerContext>Customer context</CustomerContext>
                <XpciVersion>1.0</XpciVersion>
            </TransactionReference>
            <RequestAction>Track</RequestAction>
            <RequestOption>activity</RequestOption>
        </Request>
        <{track_type}>
            <Value>{reference_number_or_tracking_number}</Value>
        </{track_type}>
    </TrackRequest>

"""

def create_xml_data(access_license_number: str, user_id: str, password: str, track_type: str, reference_number_or_tracking_number: str) -> str:
    data = __XML_REQUEST.format(
        access_license_number=access_license_number,
        user_id=user_id,
        password=password,
        track_type=track_type,
        reference_number_or_tracking_number=reference_number_or_tracking_number
    )
    
    return data
