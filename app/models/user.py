from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role: str
    full_name: str

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
