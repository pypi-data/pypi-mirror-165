from pydantic import Field
from pydantic.env_settings import BaseSettings
from pydantic.error_wrappers import ValidationError
from typing import Dict, Optional


class HumanloopSettings(BaseSettings):
    api_key: str = Field(
        title="Humanloop API key",
        description=f"Your private Humanloop API key. You can retrieve it from https://app.humanloop.com/llama/settings",
    )
    api_base_url: str = Field(
        default="https://api.humanloop.com",
        title="Humanloop API base URL",
        description=f"The Humanloop server to connect to.",
    )
    provider_api_keys: Optional[Dict[str, str]] = Field(
        title="External API keys",
        description='Insert your OpenAI key, such as \'{"OpenAI": "y0ur-AP1-K3Y-h3r3"}\'',
    )

    class Config:
        env_prefix = "HUMANLOOP_"


def get_humanloop_settings(**overrides):
    """Get settings for the Humanloop API client

    Used to read environment variables.
    """
    try:
        _settings = HumanloopSettings(**overrides)
    except ValidationError as e:
        raise ValueError(f"Failed to configure Humanloop client: {e}")
    return _settings
