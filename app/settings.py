from pydantic_settings import BaseSettings 

class Settings(BaseSettings): 
    OPENROUTER_API_KEY: str 
    OPENROUTER_MODEL: str = "tngtech/deepseek-r1t2-chimera:free" 
    OPENROUTER_BASE_URL:str="https://openrouter.ai/api/v1/chat/completions"

    
    class Config: 
        env_file = ".env" 
settings = Settings()