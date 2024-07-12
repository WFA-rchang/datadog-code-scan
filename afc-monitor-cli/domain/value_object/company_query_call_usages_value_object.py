class CompanyQueryCallUsagesValueObject:
    def __init__(self, company_name: str = None, normal_usages: int = None, 
                 channel_evaluation_usages: int = None, total_usages: int = None) -> None:
        self.company_name = company_name
        self.normal_usages = normal_usages
        self.channel_evaluation_usages = channel_evaluation_usages
        self.total_usages = total_usages
