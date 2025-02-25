from pydantic_settings import BaseSettings

import random
import string
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
class Settings(BaseSettings):
    # API Settings
    api_title: str = "Kokoro TTS API"
    api_description: str = "API for text-to-speech generation using Kokoro"
    api_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8880

    # Application Settings
    output_dir: str = "output"
    output_dir_size_limit_mb: float = 500.0  # Maximum size of output directory in MB
    default_voice: str = "af_heart"
    default_voice_code: str | None = None  # If set, overrides the first letter of voice name, though api call param still takes precedence
    use_gpu: bool = True  # Whether to use GPU acceleration if available
    allow_local_voice_saving: bool = (
        True  # Whether to allow saving combined voices locally
    )

    # Container absolute paths
    model_dir: str = "/app/api/src/models"  # Absolute path in container
    voices_dir: str = "/app/api/src/voices/v1_0"  # Absolute path in container

    # Audio Settings
    sample_rate: int = 24000
    # Text Processing Settings
    target_min_tokens: int = 175  # Target minimum tokens per chunk
    target_max_tokens: int = 250  # Target maximum tokens per chunk
    absolute_max_tokens: int = 450  # Absolute maximum tokens per chunk
    advanced_text_normalization: bool = True # Preproesses the text before misiki which leads 

    gap_trim_ms: int = 1  # Base amount to trim from streaming chunk ends in milliseconds
    dynamic_gap_trim_padding_ms: int = 410 # Padding to add to dynamic gap trim
    dynamic_gap_trim_padding_char_multiplier: dict[str,float] = {".":1,"!":0.9,"?":1,",":0.8}

    # Web Player Settings
    enable_web_player: bool = True  # Whether to serve the web player UI
    web_player_path: str = "web"  # Path to web player static files
    cors_origins: list[str] = ["*"]  # CORS origins for web player
    cors_enabled: bool = True  # Whether to enable CORS

    # Temp File Settings for WEB Ui
    temp_file_dir: str = "api/temp_files"  # Directory for temporary audio files (relative to project root)
    max_temp_dir_size_mb: int = 2048  # Maximum size of temp directory (2GB)
    max_temp_dir_age_hours: int = 1  # Remove temp files older than 1 hour
    max_temp_dir_count: int = 3  # Maximum number of temp files to keep
    auth_token: str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))

    class Config:
        env_file = ".env"

settings = Settings()
security = HTTPBearer()
print(settings.auth_token)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Authentication dependency that checks for a valid token."""
    if credentials.credentials != settings.auth_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials
