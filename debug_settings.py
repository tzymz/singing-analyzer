import os
from dotenv import load_dotenv

# 手动加载.env文件
load_dotenv()

print("=== 环境变量检查 ===")
print(f"ALIYUN_ASR_API_KEY: {os.getenv('ALIYUN_ASR_API_KEY', '未设置')}")

print("\n=== Settings配置检查 ===")
try:
    from app.core.config import settings
    print(f"settings.ALIYUN_ASR_API_KEY: {getattr(settings, 'ALIYUN_ASR_API_KEY', '未设置')}")
    print(f"settings类型: {type(settings)}")
    print(f"settings所有属性: {[attr for attr in dir(settings) if not attr.startswith('_')]}")
except Exception as e:
    print(f"导入settings失败: {e}")

print("\n=== 直接测试cloud_services ===")
try:
    from app.core.cloud_services import CloudServices
    service = CloudServices()
    print(f"fallback_mode: {service.fallback_mode}")
except Exception as e:
    print(f"测试cloud_services失败: {e}")
