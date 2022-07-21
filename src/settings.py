from pydantic import BaseSettings, Extra
import yaml
import functools

from typing import Dict, Any

OBLV_CONFIG_PATH = "/usr/runtime.yaml"


# this will read the yaml file and return it to 
# be the settings
def yaml_settings(settings: BaseSettings) -> Dict[str, Any]:
    try:
        with open(OBLV_CONFIG_PATH, 'r') as f:
            settings = yaml.safe_load(f)
    except:
        settings = {}

    return settings


class Settings(BaseSettings):

    class Config:
        # allow non-strictly defined vallues
        # to be part of the dict we extract
        # from runtime.yaml
        extra = Extra.allow

        # update the order of the settings 
        # being loaded so that we read from 
        # the runtime.yaml
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings
        ):
            return (
                init_settings,
                yaml_settings
            )


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()