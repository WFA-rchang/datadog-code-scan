from typing import List


class ServiceEndToEndRegionStatusValueObject():
    def __init__(self, region: str, status: str) -> None:
        self.region = region
        self.status = status

class ServiceEndToEndStatusValueObject():
    def __init__(self, regions_status: List[ServiceEndToEndRegionStatusValueObject] = []):
        self.regions_status = regions_status

class ServiceEndToEndDapPapRegionStatusValueObject():
    def __init__(self, monitor_name: str, region: str, status: str) -> None:
        self.monitor_name = monitor_name
        self.region = region
        self.status = status

class ServiceEndToEndDapPapStatusValueObject():
    def __init__(self, regions_status: List[ServiceEndToEndDapPapRegionStatusValueObject] = []):
        self.regions_status = regions_status
