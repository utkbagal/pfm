from .shoonya_auth import ShoonyaAuth


class ShoonyaClientFactory:

    @staticmethod
    def create(config_path: str):
        auth = ShoonyaAuth(config_path)
        return auth.login()
