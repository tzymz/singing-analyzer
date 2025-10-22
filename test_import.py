try:
    from app.api.endpoints import router
    print("✅ endpoints.py 导入成功")
    
    from app.core.cloud_services import CloudServiceManager
    print("✅ CloudServiceManager 导入成功")
    
    from app.core.config import settings
    print("✅ settings 导入成功")
    
    print("所有导入都成功了！")
    
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
