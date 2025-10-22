import aiohttp
import json
from typing import Dict, Any
import base64

class RealASRService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://funasr.cn-hangzhou.aliyuncs.com"
    
    async def transcribe_audio(self, audio_url: str) -> Dict[str, Any]:
        """使用FunASR API进行语音识别"""
        try:
            print("🎤 调用真实Fun-ASR API...")
            
            # 准备请求头
            headers = {
                "X-DashScope-Async": "enable",
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 准备请求体
            payload = {
                "model": "paraformer-realtime-v1",
                "input": {
                    "audio_url": audio_url
                },
                "parameters": {
                    "enable_punctuation": True,
                    "enable_voice_detection": True
                }
            }
            
            print(f"🔑 API Key: {self.api_key[:10]}...")
            print(f"📁 音频URL: {audio_url[:80]}...")
            
            async with aiohttp.ClientSession() as session:
                # 发送识别请求
                print("🚀 发送API请求...")
                async with session.post(
                    f"{self.base_url}/api/v1/recognize",
                    headers=headers,
                    json=payload
                ) as response:
                    
                    print(f"📡 API响应状态: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        print("✅ API调用成功，获取任务ID")
                        return result
                    else:
                        error_text = await response.text()
                        print(f"❌ API调用失败: {error_text}")
                        return {"error": f"API调用失败: {response.status}"}
                        
        except Exception as e:
            print(f"❌ FunASR服务异常: {e}")
            return {"error": str(e)}
    
    async def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """查询任务结果"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/tasks/{task_id}",
                    headers=headers
                ) as response:
                    
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"error": f"查询失败: {response.status}"}
                        
        except Exception as e:
            return {"error": str(e)}
