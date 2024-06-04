class CompanyQueryCallUsagesValueObject():
    def __init__(self, company_name: str = None, usages: int = None) -> None:
        self.company_name = company_name
        self.usages = usages
