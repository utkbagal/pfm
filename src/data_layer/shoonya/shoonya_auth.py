import json
import os
import pyotp
from pathlib import Path
from dotenv import load_dotenv
from NorenRestApiPy.NorenApi import NorenApi


class ShoonyaAuthError(Exception):
    pass


class ShoonyaAuth:
    """
    Handles Shoonya login and session creation
    """

    def __init__(self, config_path: str):
        load_dotenv()
        self.config = self._load_config(config_path)
        self.api = NorenApi()

    def login(self) -> NorenApi:
        try:
            totp = self._generate_totp()

            response = self.api.login(
                userid=self.config["user_id"],
                password=self.config["password"],
                twoFA=totp,
                vendor_code=self.config["vendor_code"],
                api_secret=self.config["api_key"],
                imei=self.config["imei"]
            )

            if response is None or response.get("stat") != "Ok":
                raise ShoonyaAuthError(
                    f"Shoonya login failed: {response}"
                )

            return self.api

        except Exception as e:
            raise ShoonyaAuthError(str(e)) from e

    def _generate_totp(self) -> str:
        secret = self.config.get("totp_secret")
        if not secret:
            raise ShoonyaAuthError("TOTP secret missing")

        return pyotp.TOTP(secret).now()

    @staticmethod
    def _load_config(path: str) -> dict:
        with open(Path(path), "r", encoding="utf-8") as f:
            raw = json.load(f)

        config = {}
        for key, value in raw.items():
            if isinstance(value, str) and value.startswith("${"):
                env_key = value.strip("${}")
                config[key] = os.getenv(env_key)
            else:
                config[key] = value

        missing = [k for k, v in config.items() if not v]
        if missing:
            raise ShoonyaAuthError(
                f"Missing Shoonya config values: {missing}"
            )

        return config
