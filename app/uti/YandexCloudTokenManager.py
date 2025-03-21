import subprocess
import time

class YandexCloudTokenManager:
    def __init__(self):
        self.token = None
        self.token_expiry = 0
        self.token_lifetime = 3600  # 1 час

    def get_token(self):
        current_time = time.time()
        if self.token is None or current_time >= self.token_expiry:
            self.token = self.create_new_token()
            self.token_expiry = current_time + self.token_lifetime
        return self.token

    def create_new_token(self):
        result = subprocess.run(['yc', 'iam', 'create-token'], stdout=subprocess.PIPE)
        token = result.stdout.decode('utf-8').strip()
        return token
