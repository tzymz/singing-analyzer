import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI唱歌分析"
    
    # 阿里云OSS配置
    ALIYUN_ACCESS_KEY_ID: str = os.getenv("ALIYUN_ACCESS_KEY_ID", "test_key")
    ALIYUN_ACCESS_KEY_SECRET: str = os.getenv("ALIYUN_ACCESS_KEY_SECRET", "test_secret")
    ALIYUN_OSS_BUCKET: str = os.getenv("ALIYUN_OSS_BUCKET", "test_bucket")
    ALIYUN_OSS_ENDPOINT: str = os.getenv("ALIYUN_OSS_ENDPOINT", "oss-cn-hangzhou.aliyuncs.com")
    ALIYUN_NLS_APP_KEY: str = os.getenv("ALIYUN_NLS_APP_KEY", "test_app_key")
    
    # Fun-ASR API配置
    ALIYUN_ASR_API_KEY: str = os.getenv("ALIYUN_ASR_API_KEY", "sk-436f4d6bf2814b87aa8ad4418b1bcb3a")

settings = Settings()


