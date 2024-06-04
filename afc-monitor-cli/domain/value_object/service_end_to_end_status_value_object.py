from typing import List


class ServiceEndToEndRegionStatusValueObject():
    def __init__(self, region: str, status: str) -> None:
        self.region = region
        self.status = status

class ServiceEndToEndStatusValueObject():
    def __init__(self, regions_status: List[ServiceEndToEndRegionStatusValueObject] = []):
        self.regions_status = regions_status
