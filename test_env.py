import os
print("环境变量检查:")
print(f"ALIYUN_API_KEY: {os.getenv('ALIYUN_API_KEY', '未设置')}")
print(f"ALIYUN_ASR_API_KEY: {os.getenv('ALIYUN_ASR_API_KEY', '未设置')}")
print(f"ALIYUN_OSS_BUCKET: {os.getenv('ALIYUN_OSS_BUCKET', '未设置')}")

# 检查是否在settings模块中
try:
    from app.core.config import settings
    print(f"settings.ALIYUN_ASR_API_KEY: {getattr(settings, 'ALIYUN_ASR_API_KEY', '未设置')}")
except Exception as e:
    print(f"导入settings失败: {e}")
