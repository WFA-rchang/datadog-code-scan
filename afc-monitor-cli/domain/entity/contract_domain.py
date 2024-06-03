class ContractDomain():
    def __init__(self, id: int = None, contract_group_id: int = None,
                 monthly_bucket: int = None):
        self.id = id
        self.contract_group_id = contract_group_id
        self.monthly_bucket = monthly_bucket
