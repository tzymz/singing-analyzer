from typing import Dict, Any, List
from app.core.cloud_services import CloudServiceManager

class AnalysisService:
    def __init__(self, cloud_manager: CloudServiceManager):
        self.cloud_manager = cloud_manager
    
    async def comprehensive_analysis(self, audio_data: bytes, user_level: str = "beginner") -> Dict[str, Any]:
        """综合音频分析"""
        print(f"开始分析音频，用户水平: {user_level}")
        
        # 上传音频
        audio_url = await self.cloud_manager.upload_audio(audio_data)
        
        # 调用云服务分析
        cloud_result = await self.cloud_manager.analyze_singing(audio_url)
        
        # 生成报告
        return await self._generate_report(cloud_result, user_level)
    
    async def _generate_report(self, cloud_data: Dict, user_level: str) -> Dict[str, Any]:
        """生成分析报告"""
        scores = {
            "pitch_accuracy": cloud_data.get("pronunciation", {}).get("score", 0) * 100,
            "rhythm_accuracy": cloud_data.get("rhythm", {}).get("score", 0) * 100,
            "completeness": cloud_data.get("completeness", 0) * 100,
            "fluency": cloud_data.get("fluency", 0) * 100
        }
        
        # 生成反馈
        feedback = self._generate_feedback(scores, user_level)
        
        return {
            "technical_scores": scores,
            "personalized_feedback": feedback,
            "improvement_plan": self._create_plan(scores, user_level),
            "overall_score": sum(scores.values()) / len(scores)
        }
    
    def _generate_feedback(self, scores: Dict, user_level: str) -> List[str]:
        """生成反馈建议"""
        feedback = []
        
        if scores["pitch_accuracy"] < 70:
            feedback.append("🎵 音准需要加强，建议进行音阶练习")
        
        if scores["rhythm_accuracy"] < 75:
            feedback.append("🥁 节奏稳定性有待提高，尝试使用节拍器练习")
        
        if len(feedback) == 0:
            feedback.append("🎉 表现不错！继续保持练习")
        
        return feedback
    
    def _create_plan(self, scores: Dict, user_level: str) -> Dict[str, Any]:
        """创建改进计划"""
        exercises = []
        
        if scores["pitch_accuracy"] < 70:
            exercises.append("基础音阶练习 - 每天10分钟")
        
        if scores["rhythm_accuracy"] < 75:
            exercises.append("节拍器跟拍练习 - 每天8分钟")
        
        return {
            "daily_exercises": exercises,
            "recommended_songs": self._get_recommended_songs(user_level)
        }
    
    def _get_recommended_songs(self, user_level: str) -> List[str]:
        """推荐歌曲"""
        if user_level == "beginner":
            return ["小星星", "欢乐颂", "童年"]
        elif user_level == "intermediate":
            return ["月亮代表我的心", "成都", "青花瓷"]
        else:
            return ["泡沫", "不为谁而作的歌"]



