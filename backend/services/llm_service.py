# LLM Service - Groq API Integration
import httpx
import os
from typing import Dict, Any, List, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Simple settings class to avoid import issues"""
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

settings = Settings()


class LLMService:
    """LLM Service using Groq API with openai/gpt-oss-120b model"""
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.base_url = settings.GROQ_BASE_URL
        self.model = settings.GROQ_MODEL
    
    async def _call_llm(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> str:
        """Make API call to Groq"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            # Fallback response for demo/development
            return self._get_fallback_response(messages[-1]["content"])
    
    def _get_fallback_response(self, query: str) -> str:
        """Fallback response when API is unavailable"""
        return f"I understand you're asking about: {query}. Please ensure your Groq API key is configured to get AI-powered insights."
    
    async def generate_summary(
        self,
        metrics: Dict[str, Any],
        scores: Dict[str, Any],
        industry: str,
        language: str = "en"
    ) -> str:
        """Generate AI CFO-style summary of financial health"""
        
        # Determine health status with emoji
        overall_score = scores.get('overall_score', 0)
        if overall_score >= 75:
            status_line = f"✅ Your business is financially healthy (Score: {overall_score}/100)"
        elif overall_score >= 50:
            status_line = f"⚠️ Your business is stable but needs attention (Score: {overall_score}/100)"
        else:
            status_line = f"🔴 Your business needs immediate financial attention (Score: {overall_score}/100)"
        
        lang_instruction = "Respond in Hindi with key financial terms in English." if language == "hi" else "Respond in English."
        
        prompt = f"""You are an AI CFO providing a financial health summary for a {industry} business owner.

FINANCIAL STATUS:
{status_line}
Grade: {scores.get('grade', 'N/A')} | Risk Level: {scores.get('risk_level', 'Unknown')}

KEY NUMBERS:
- Liquidity (Current Ratio): {metrics.get('current_ratio', 0):.2f}
- Profit Margin: {metrics.get('net_margin', 0):.1f}%
- Debt Level: {metrics.get('debt_to_equity', 0):.2f}
- Cash Runway: {metrics.get('cash_runway_days', 0)} days

{lang_instruction}

Write a CFO-style summary using EXACTLY this format:

**Overall:** [1 sentence - are they safe? healthy? at risk?]

**✅ Strengths:**
• [strength 1 with specific number]
• [strength 2 with specific number]

**⚠️ Areas to Watch:**
• [risk/concern 1 with action hint]
• [risk/concern 2 if applicable]

**📌 Your Next Step:**
[1 specific action to improve financial health]

Keep it under 120 words. Be encouraging but honest. No jargon."""

        messages = [{"role": "user", "content": prompt}]
        return await self._call_llm(messages, max_tokens=400)
    
    async def generate_recommendations(
        self,
        metrics: Dict[str, Any],
        scores: Dict[str, Any],
        industry: str,
        language: str = "en"
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        
        lang_instruction = "Respond in Hindi with some English terms." if language == "hi" else "Respond in English."
        
        prompt = f"""You are a financial advisor for SME business owners.

Based on this financial data, provide specific, actionable recommendations:

**Industry:** {industry}
**Health Score:** {scores.get('overall_score', 0)}/100
**Risk Level:** {scores.get('risk_level', 'Unknown')}

**Scores Breakdown:**
- Liquidity: {scores.get('liquidity_score', 0)}/100
- Profitability: {scores.get('profitability_score', 0)}/100
- Solvency: {scores.get('solvency_score', 0)}/100
- Efficiency: {scores.get('efficiency_score', 0)}/100
- Cash Flow: {scores.get('cash_flow_score', 0)}/100

**Key Metrics:**
- Cash Runway: {metrics.get('cash_runway_days', 0)} days
- Net Margin: {metrics.get('net_margin', 0):.1f}%
- Working Capital Cycle: {metrics.get('working_capital_cycle', 0)} days

{lang_instruction}

Provide exactly 5 recommendations in this JSON format:
[
  {{"priority": "high/medium/low", "category": "category", "title": "short title", "description": "detailed actionable advice", "expected_impact": "what improvement to expect"}}
]

Focus on practical actions the business owner can take immediately."""

        messages = [{"role": "user", "content": prompt}]
        response = await self._call_llm(messages, max_tokens=800)
        
        try:
            # Try to parse JSON from response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        # Return default recommendations if parsing fails
        return self._get_default_recommendations(scores)
    
    def _get_default_recommendations(self, scores: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Default recommendations based on scores"""
        recommendations = []
        
        if scores.get("liquidity_score", 100) < 60:
            recommendations.append({
                "priority": "high",
                "category": "Liquidity",
                "title": "Improve Cash Position",
                "description": "Consider collecting receivables faster or negotiating better payment terms with suppliers.",
                "expected_impact": "Better ability to meet short-term obligations"
            })
        
        if scores.get("profitability_score", 100) < 60:
            recommendations.append({
                "priority": "high",
                "category": "Profitability",
                "title": "Review Pricing Strategy",
                "description": "Analyze your pricing and cost structure to improve margins.",
                "expected_impact": "Increased profit margins"
            })
        
        if scores.get("cash_flow_score", 100) < 60:
            recommendations.append({
                "priority": "high",
                "category": "Cash Flow",
                "title": "Extend Cash Runway",
                "description": "Build a cash reserve of at least 3-6 months of operating expenses.",
                "expected_impact": "Better financial security"
            })
        
        # Add general recommendations
        recommendations.append({
            "priority": "medium",
            "category": "Growth",
            "title": "Explore Financing Options",
            "description": "Based on your profile, explore working capital loans or lines of credit.",
            "expected_impact": "Access to growth capital"
        })
        
        recommendations.append({
            "priority": "low",
            "category": "Compliance",
            "title": "Review Tax Efficiency",
            "description": "Ensure you're utilizing all available tax deductions and credits.",
            "expected_impact": "Reduced tax burden"
        })
        
        return recommendations[:5]
    
    async def identify_risks(
        self,
        metrics: Dict[str, Any],
        scores: Dict[str, Any],
        industry: str,
        language: str = "en"
    ) -> List[Dict[str, Any]]:
        """Identify financial risks"""
        
        risks = []
        
        # Liquidity risk
        if metrics.get("current_ratio", 2) < 1.0:
            risks.append({
                "name": "Liquidity Risk",
                "severity": "high",
                "description": "Current assets may not cover short-term obligations",
                "indicator": f"Current Ratio: {metrics.get('current_ratio', 0):.2f}"
            })
        
        # Cash flow risk
        if metrics.get("cash_runway_days", 365) < 90:
            risks.append({
                "name": "Cash Flow Risk",
                "severity": "critical" if metrics.get("cash_runway_days", 365) < 30 else "high",
                "description": "Limited cash runway could affect operations",
                "indicator": f"Cash Runway: {metrics.get('cash_runway_days', 0)} days"
            })
        
        # Profitability risk
        if metrics.get("net_margin", 10) < 0:
            risks.append({
                "name": "Profitability Risk",
                "severity": "high",
                "description": "Operating at a loss affects sustainability",
                "indicator": f"Net Margin: {metrics.get('net_margin', 0):.1f}%"
            })
        
        # Debt risk
        if metrics.get("debt_to_equity", 0) > 2.0:
            risks.append({
                "name": "Leverage Risk",
                "severity": "medium",
                "description": "High debt levels increase financial vulnerability",
                "indicator": f"Debt-to-Equity: {metrics.get('debt_to_equity', 0):.2f}"
            })
        
        # Efficiency risk
        if metrics.get("working_capital_cycle", 60) > 90:
            risks.append({
                "name": "Working Capital Risk",
                "severity": "medium",
                "description": "Long cash conversion cycle ties up capital",
                "indicator": f"WC Cycle: {metrics.get('working_capital_cycle', 0)} days"
            })
        
        return risks
    
    async def answer_question(
        self,
        question: str,
        context: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        language: str = "en"
    ) -> str:
        """Answer natural language questions about financial data - AI CFO Style"""
        
        # Extract key financial insights for structured context
        health_score = context.get('health_score', 0)
        grade = context.get('grade', 'N/A')
        company_name = context.get('company_name', 'Your Company')
        industry = context.get('industry', 'business')
        metrics = context.get('metrics', {})
        risks = context.get('risks', [])
        forecast = context.get('forecast', {})
        recommendations = context.get('recommendations', [])
        
        # Determine financial health status
        if health_score >= 75:
            health_status = "strong and healthy"
            health_emoji = "✅"
        elif health_score >= 50:
            health_status = "stable but with room for improvement"
            health_emoji = "⚠️"
        else:
            health_status = "needs attention"
            health_emoji = "🔴"
        
        # Format risks as readable list
        risk_summary = ""
        if risks:
            risk_items = []
            for risk in risks[:3]:
                if isinstance(risk, dict):
                    risk_items.append(f"• {risk.get('name', 'Unknown risk')}: {risk.get('description', '')}")
                elif isinstance(risk, str):
                    risk_items.append(f"• {risk}")
            risk_summary = "\n".join(risk_items) if risk_items else "No major risks identified."
        else:
            risk_summary = "No major risks identified."
        
        # Language instruction
        lang_instruction = "Respond in Hindi with key financial terms in English." if language == "hi" else "Respond in English."
        
        # Enterprise AI CFO System Prompt
        system_prompt = f"""You are an AI CFO (Chief Financial Officer) for {company_name}, a {industry} business.

FINANCIAL SNAPSHOT:
{health_emoji} Health Score: {health_score}/100 (Grade: {grade})
Status: The business is {health_status}.

KEY METRICS:
{json.dumps(metrics, indent=2) if metrics else "Limited data available."}

IDENTIFIED RISKS:
{risk_summary}

FORECAST DATA:
{json.dumps(forecast, indent=2) if forecast else "Forecasts unavailable - incomplete data."}

---

YOUR BEHAVIOR RULES:

1. YOU ARE AN AI CFO - Speak like a trusted financial advisor, not a textbook.

2. EVERY RESPONSE MUST ANSWER:
   - What is happening? (current situation)
   - Why is it happening? (cause/context)
   - What should they do next? (actionable steps)

3. RESPONSE FORMAT:
   - Start with a clear 1-2 sentence summary
   - Use bullet points for lists (✅ for strengths, ⚠️ for risks, 📌 for actions)
   - Keep responses concise - no text walls
   - End with a specific actionable recommendation

4. TONE GUIDELINES:
   - Conversational and friendly
   - Avoid financial jargon - use plain business language
   - Be specific with numbers when available
   - Be encouraging but honest about problems

5. RESPONSE TYPES:
   - Quick questions: 2-4 sentences
   - Analysis questions: Bullet points with summary
   - Decision questions: Clear recommendation with reasoning

6. NEVER:
   - Dump raw numbers without explanation
   - Use complex financial terminology
   - Give vague advice like "improve efficiency"
   - Write more than 150 words unless specifically asked for detail

{lang_instruction}

Remember: Business owners want to know "Am I safe?" and "What should I do?" - answer those questions."""

        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 5 messages for context)
        for msg in conversation_history[-5:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": question})
        
        return await self._call_llm(messages, max_tokens=500)
    
    async def suggest_questions(
        self,
        context: Dict[str, Any],
        last_question: str,
        language: str = "en"
    ) -> List[str]:
        """Suggest follow-up questions"""
        
        # Context-aware suggestions based on data
        suggestions = []
        
        metrics = context.get("metrics", {})
        risks = context.get("risks", [])
        
        # Add risk-based questions
        for risk in risks[:2]:
            if isinstance(risk, dict):
                suggestions.append(f"How can I reduce my {risk.get('name', 'risk')}?")
        
        # Add general questions
        base_suggestions = [
            "What should I focus on to improve my score?",
            "Is my business ready for expansion?",
            "How do I compare to others in my industry?",
            "What's my expected revenue next quarter?",
            "Should I apply for a business loan?"
        ]
        
        suggestions.extend(base_suggestions)
        
        # Return top 4 unique suggestions
        return list(dict.fromkeys(suggestions))[:4]
    
    async def query_financial_data(
        self,
        query: str,
        context: Dict[str, Any],
        conversation_history: List[Dict[str, str]] = None,
        language: str = "en"
    ) -> str:
        """Query financial data with natural language - wrapper for chat router"""
        
        # Build enhanced context for the question
        enhanced_context = {
            "company_name": context.get("company_name", "Your Company"),
            "industry": context.get("industry", "General"),
            "health_score": context.get("overall_score", 0),
            "grade": context.get("score_grade", "N/A"),
            "metrics": context.get("metrics", {}),
            "risks": context.get("risk_factors", []),
            "forecast": context.get("forecast_data", {}),
            "recommendations": context.get("recommendations", []),
            "summary": context.get("summary", "")
        }
        
        return await self.answer_question(
            question=query,
            context=enhanced_context,
            conversation_history=conversation_history or [],
            language=language
        )

