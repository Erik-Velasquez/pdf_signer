from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "PDF Signer"
    version: str = "1.0.0"
    max_upload_size: int = 10 * 1024 * 1024  # 10 MB


settings = Settings()
