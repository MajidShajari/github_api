class Settings:
    PROJECT_NAME: str = "Github Api 🔥"
    PROJECT_VERSION: str = "1.0.0"
    BASE_DIR: str = "app"
    TEMPLETE_DIRECTORY: str = BASE_DIR + "/templates"
    STATIC_DIRECTORY: str = BASE_DIR + "/static"
    ORIGINS = ["*"]


settings = Settings()
