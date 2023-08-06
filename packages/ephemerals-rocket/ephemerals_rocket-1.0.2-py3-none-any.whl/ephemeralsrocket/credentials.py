class Credentials:
    name: str
    secret: str
    grant_type: str

    def __init__(self, name: str, secret: str, grant_type: str):
        self.name = name
        self.secret = secret
        self.grant_type = grant_type
