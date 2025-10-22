import requests

# 测试健康检查
response = requests.get("http://localhost:8000/health")
print(f"健康检查: {response.status_code} - {response.json()}")

# 测试API根路径  
response = requests.get("http://localhost:8000/api")
print(f"API根路径: {response.status_code} - {response.json()}")

# 测试上传接口（不带文件）
try:
    response = requests.post("http://localhost:8000/api/upload-audio")
    print(f"上传接口(/api/upload-audio): {response.status_code}")
except:
    print("上传接口(/api/upload-audio): 连接失败")

# 测试另一个可能的路径
try:
    response = requests.post("http://localhost:8000/upload-audio")
    print(f"上传接口(/upload-audio): {response.status_code}")
except:
    print("上传接口(/upload-audio): 连接失败")
