"""
Chat Router - Natural language querying with LLM
"""
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import User, Company, HealthScore
from services.llm_service import LLMService
from routers.auth import get_current_user

router = APIRouter()

# Schemas
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    company_id: int
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    suggested_questions: Optional[List[str]] = []

# Initialize LLM service
llm_service = LLMService()

@router.post("/query", response_model=ChatResponse)
async def chat_query(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Natural language query about financial data"""
    # Verify company ownership
    company = db.query(Company).filter(
        Company.id == request.company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get latest health score for context
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == request.company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    # Build context from stored data
    context = build_context(company, health_score)
    
    # Convert conversation history
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in (request.conversation_history or [])
    ]
    
    # Get LLM response
    try:
        response = await llm_service.query_financial_data(
            query=request.message,
            context=context,
            conversation_history=history
        )
        
        # Generate follow-up suggestions
        suggestions = generate_suggestions(request.message, health_score)
        
        return ChatResponse(
            response=response,
            suggested_questions=suggestions
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )

def build_context(company: Company, health_score: Optional[HealthScore]) -> dict:
    """Build context dictionary for LLM"""
    context = {
        "company_name": company.name,
        "industry": company.industry
    }
    
    if health_score:
        context.update({
            "overall_score": health_score.overall_score,
            "score_grade": health_score.score_grade,
            "risk_level": health_score.risk_level,
            "liquidity_score": health_score.liquidity_score,
            "profitability_score": health_score.profitability_score,
            "solvency_score": health_score.solvency_score,
            "efficiency_score": health_score.efficiency_score,
            "cash_flow_score": health_score.cash_flow_score,
            "industry_percentile": health_score.industry_percentile,
            "summary": health_score.summary,
            "metrics": json.loads(health_score.metrics) if health_score.metrics else {},
            "risk_factors": json.loads(health_score.risk_factors) if health_score.risk_factors else [],
            "recommendations": json.loads(health_score.recommendations) if health_score.recommendations else [],
            "benchmark_data": json.loads(health_score.benchmark_data) if health_score.benchmark_data else {},
            "forecast_data": json.loads(health_score.forecast_data) if health_score.forecast_data else {}
        })
    
    return context

def generate_suggestions(query: str, health_score: Optional[HealthScore]) -> List[str]:
    """Generate contextual follow-up question suggestions"""
    suggestions = []
    
    if not health_score:
        return [
            "How do I upload my financial data?",
            "What file formats are supported?",
            "How is the health score calculated?"
        ]
    
    query_lower = query.lower()
    
    # Context-aware suggestions
    if "score" in query_lower:
        suggestions.extend([
            "How can I improve my score?",
            "Which area needs the most attention?",
            "How does my score compare to industry?"
        ])
    elif "risk" in query_lower:
        suggestions.extend([
            "What should I do to reduce risks?",
            "Which risk is most urgent?",
            "How do risks affect my funding options?"
        ])
    elif "cash" in query_lower or "flow" in query_lower:
        suggestions.extend([
            "How can I improve cash flow?",
            "What is my cash runway?",
            "When might I face cash shortage?"
        ])
    elif "benchmark" in query_lower or "industry" in query_lower:
        suggestions.extend([
            "Where do I outperform competitors?",
            "What are typical ratios for my industry?",
            "How can I reach top quartile?"
        ])
    else:
        # General suggestions based on data
        if health_score.risk_level in ["High", "Critical"]:
            suggestions.append("What are my main risk factors?")
        if health_score.overall_score < 60:
            suggestions.append("How can I improve my health score?")
        if health_score.cash_flow_score < 50:
            suggestions.append("How can I improve cash flow?")
        
        suggestions.extend([
            "Give me a summary of my financial health",
            "What financing options are available to me?",
            "What should be my top priority?"
        ])
    
    return suggestions[:4]  # Return max 4 suggestions

@router.get("/suggested-questions/{company_id}")
async def get_suggested_questions(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get suggested questions for a company"""
    # Verify ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    questions = []
    
    if not health_score:
        questions = [
            "How do I get started?",
            "What documents do I need to upload?",
            "How is the health score calculated?"
        ]
    else:
        # Personalized questions based on data
        questions.append(f"Explain my health score of {health_score.overall_score}")
        
        if health_score.risk_level in ["High", "Critical"]:
            questions.append("What are my major risk factors?")
        
        if health_score.overall_score < 70:
            questions.append("How can I improve my financial health?")
        
        questions.extend([
            "How do I compare to industry benchmarks?",
            "What financing options should I consider?",
            "What's my 12-month financial forecast?"
        ])
    
    return {"questions": questions[:6]}
