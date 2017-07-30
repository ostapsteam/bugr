class Update:

    def __init__(self, msg):
        self._msg = msg

    def get_text(self):
        return self._msg["message"]["text"]

    def get_chat_id(self):
        return self._msg["message"]["chat"]["id"]

    @property
    def id(self):
        return self._msg["update_id"]

    @property
    def sender(self):
        return self._msg["message"]["from"]
    
    def prepare_command(self):
        parts = self.get_text().split()
        if parts:
            cmd = parts[0]
            if len(cmd) > 1 and cmd.startswith("/"):
                return parts
