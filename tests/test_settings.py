from fastapi.testclient import TestClient
from app import app

# general import so we can override 
# the get_settings
import settings
import json

client = TestClient(app)

def get_settings():
    return settings.Settings(hello="world")

# override settings globally to mock for tests
settings.get_settings = get_settings

def test_settings():
    response = client.get(
        "/settings"
    )

    settings_dict = json.loads(response.content)

    assert settings_dict["hello"] == "world"

