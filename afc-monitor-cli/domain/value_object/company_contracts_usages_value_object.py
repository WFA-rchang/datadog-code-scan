from typing import List


class MonthlyBucketUsageValueObject():
    def __init__(self, month: int, licensed_count: int):
        self.month = month
        self.licensed_count = licensed_count

class ContractGroupUsagesValueObject():
    def __init__(self, comtract_group_id: int, monthly_buckets: List[MonthlyBucketUsageValueObject]):
        self.comtract_group_id = comtract_group_id
        self.monthly_buckets = monthly_buckets

class CompanyContractsUsagesValueObject():
    def __init__(self, company_name: str, contract_groups: List[ContractGroupUsagesValueObject]):
        self.company_name = company_name
        self.contract_groups = contract_groups
