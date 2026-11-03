import httpx
from typing import List, Dict, Any
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.api_base = settings.LLM_API_BASE
        self.model = settings.LLM_MODEL

    def _build_resume_prompt(self, resume_data: Dict[str, Any]) -> str:
        name = resume_data.get('name', '未填写')
        phone = resume_data.get('phone', '未填写')
        email = resume_data.get('email', '未填写')
        education_list = resume_data.get('educationList', [])
        experience_list = resume_data.get('experienceList', [])
        skill_list = resume_data.get('skillList', [])
        certificate_list = resume_data.get('certificateList', [])
        strengths = resume_data.get('strengths', '未填写')

        education_str = "\n".join([
            f"- {e.get('school', '')} {e.get('major', '')} {e.get('degree', '')} ({e.get('startDate', '')}-{e.get('endDate', '')})"
            for e in education_list
        ]) if education_list else "未填写"

        experience_str = "\n".join([
            f"- {e.get('title', '')} @ {e.get('company', '')} ({e.get('startDate', '')}-{e.get('endDate', '')}): {e.get('description', '')}"
            for e in experience_list
        ]) if experience_list else "未填写"

        skills_str = ", ".join(skill_list) if skill_list else "未填写"

        cert_str = ", ".join([c.get('name', '') for c in certificate_list]) if certificate_list else "未填写"

        prompt = f"""你是一位资深HR专家，请分析以下简历并给出改进建议。

【简历信息】
姓名: {name}
联系方式: {phone} / {email}

【教育经历】
{education_str}

【实习/项目经历】
{experience_str}

【专业技能】
{skills_str}

【证书/荣誉】
{cert_str}

【个人优势】
{strengths}

请从以下几个维度给出具体、可操作的建议（每条建议不超过50字）：
1. 教育背景评价与建议
2. 实习/项目经验评价与建议
3. 技能展示评价与建议
4. 证书与荣誉评价与建议
5. 个人优势评价与建议
6. 其他综合建议

请用JSON格式返回，格式如下：
{{"suggestions": ["建议1", "建议2", ...]}}
只返回JSON，不要有其他内容。"""
        return prompt

    async def generate_resume_suggestions(self, resume_data: Dict[str, Any]) -> List[str]:
        if not self.api_key:
            return []

        prompt = self._build_resume_prompt(resume_data)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一位专业的HR顾问，每次分析时请从不同角度给出建议，确保每次回复有所不同。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 1.0,
            "max_tokens": 1000
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    json=payload
                )
                if response.status_code == 200:
                    result = response.json()
                    content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    import json
                    try:
                        data = json.loads(content)
                        return data.get('suggestions', [])
                    except:
                        return [content]
                return []
        except Exception as e:
            print(f"LLM API Error: {e}")
            return []


llm_service = LLMService()
