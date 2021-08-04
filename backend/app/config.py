import os

from functools import lru_cache
from pydantic import BaseSettings


# ref: https://fastapi.tiangolo.com/advanced/settings/

class Settings(BaseSettings):
    secret_key: str = '03fbc8b75667bd504d73f9280fcbf9dcb1f810f44d2c5e3e1d710799de68d223'
    algorithm: str = 'HS256'
    access_token_expire_minute: int = 30
    database_host: str = '127.0.0.1'
    database_port: str = '5432'

    def settings_dict(self):
        # returns the dictionary form of Settings
        return {
                "secret_key"  : self.secret_key,
                "algorithm"  : self.algorithm,
                "access_token_expire_minute"  : self.access_token_expire_minute,
                "database_host"  : self.database_host,
                "database_port"  : self.database_port  
                }
    
    class Config:
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        env_file = os.path.join(parent_dir, '.env_backend')


@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()