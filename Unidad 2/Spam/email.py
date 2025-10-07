# ---------------------------
# 1) Representación del correo
# ---------------------------

class Email:
    subject: str
    sender: str
    body: str
    attachments: List[str]
    label: str

    def urls(self) -> List[str]:
        url_regex = r"(https?://[^\s]+)"
        return re.findall(url_regex, self.body, flags=re.I)
