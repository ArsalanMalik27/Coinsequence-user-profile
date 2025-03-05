from pydantic import BaseSettings


class MasterdataSettings(BaseSettings):
    BASE_URL: str = "http://masterdata-web.masterdata:8000"
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True
        env_nested_delimiter = "__"
        env_file = ".env"


masterdata_settings = MasterdataSettings()
