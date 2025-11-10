from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    app_name: str = "StatcheckAPI"
    debug: bool = False
    db_host: str = ""
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""

    @property
    def db_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
    

config = Config()
