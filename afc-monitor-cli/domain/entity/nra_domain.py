class NRADomain():
    def __init__(self, id: int = None, certification_id: str = None, is_authed: bool = None,
                 ruleset_id: str = None, deployment_type: int = None):
        self.id = id
        self.certification_id = certification_id
        self.is_authed = is_authed
        self.ruleset_id = ruleset_id
        self.deployment_type = deployment_type
