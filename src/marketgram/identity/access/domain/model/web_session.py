from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
    

@dataclass
class WebSession:
    user_id: UUID
    session_id: UUID
    created_at: datetime
    expires_in: datetime
    device: str

    def is_living(self, current_time: datetime) -> None:
        return (self.expires_in - current_time).days <= 1

    def to_formatted_time(self) -> str:
        return self.expires_in.strftime('%a, %d %b %Y %H:%M:%S')
    
    def to_string_id(self) -> str:
        return str(self.session_id)

    def for_browser(self) -> dict[str, str]:
        return {
            'user_id': str(self.user_id),
            'session_id': self.to_string_id(),
            'expires_in': self.to_formatted_time()
        }