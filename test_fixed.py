import os
from dotenv import load_dotenv
load_dotenv()

print("=== 使用正确类名测试 ===")
print(f"ALIYUN_ASR_API_KEY: {os.getenv('ALIYUN_ASR_API_KEY')}")

try:
    from app.core.config import settings
    print(f"settings.ALIYUN_ASR_API_KEY: {settings.ALIYUN_ASR_API_KEY}")
    
    # 使用正确的类名
    from app.core.cloud_services import CloudServiceManager
    service = CloudServiceManager()
    print(f"✅ 服务初始化成功")
    print(f"fallback_mode: {service.fallback_mode}")
    
    # 检查初始化日志
    print("\n=== 服务初始化详情 ===")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
