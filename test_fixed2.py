import os
from dotenv import load_dotenv
load_dotenv()

print("=== 使用正确参数测试 ===")

try:
    from app.core.config import settings
    print(f"settings.ALIYUN_ASR_API_KEY: {settings.ALIYUN_ASR_API_KEY}")
    
    # 使用正确的类名和参数
    from app.core.cloud_services import CloudServiceManager
    service = CloudServiceManager(settings)  # 传入settings参数
    print(f"✅ 服务初始化成功")
    print(f"fallback_mode: {service.fallback_mode}")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
