from dataclasses import dataclass
from typing import List, Optional
import re

# =========================================================
# Modelo de email
# =========================================================

URL_REGEX = re.compile(r"https?://[^\s)>\]]+", flags=re.I)

@dataclass
class Email:
    subject: str
    sender: str
    body: str
    attachments: List[str]
    label: Optional[str] = None

    def urls(self) -> List[str]:
        text = f"{self.subject}\n{self.body}"
        return URL_REGEX.findall(text)

