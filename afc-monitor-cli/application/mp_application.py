from abc import ABC, abstractmethod


class MPApplication(ABC):
    @abstractmethod
    def get_nras():
        pass

    @abstractmethod
    def get_companies_contracts_usages():
        pass

    @abstractmethod
    def get_registered_devices_in_period(period: str = '1d'):
        pass
