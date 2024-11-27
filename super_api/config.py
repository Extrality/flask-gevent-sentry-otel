from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class Settings(BaseSettings):
    # Also see gunicorn.conf.py for additional configuration options
    model_config = SettingsConfigDict(
        toml_file="settings.dev-local.toml",
        env_prefix="SUPER_",
        env_nested_delimiter="__",
    )

    secret_key: str
    python_logger_level: str = "INFO"
    debug: bool = False
    testing: bool = False

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # return (env_settings, init_settings, file_secret_settings)
        return (env_settings, TomlConfigSettingsSource(settings_cls))


settings = Settings()
