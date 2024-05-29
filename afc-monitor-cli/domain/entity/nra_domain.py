class NRADomain():
    def __init__(self, id: int, certification_id: str, is_authed: bool,
                 ruleset_id: str, deployment_type: int):
        self.id = id
        self.certification_id = certification_id
        self.is_authed = is_authed
        self.ruleset_id = ruleset_id
        self.deployment_type = deployment_type
