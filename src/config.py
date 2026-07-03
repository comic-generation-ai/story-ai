import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load env variables from a local .env file
load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY", "")
    BASE_URL = os.getenv("BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "qwen-plus")
    PORT = int(os.getenv("PORT", "50052"))
    HOST = os.getenv("HOST", "localhost")

    @classmethod
    def validate(cls):
        if not cls.API_KEY:
            print("WARNING: API_KEY is not set. story-ai will fallback to mock mode.")
