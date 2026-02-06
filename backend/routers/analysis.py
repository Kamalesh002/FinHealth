"""
Analysis Router - Financial health scoring, benchmarks, and forecasts
"""
import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from models import User, Company, FinancialData, HealthScore
from services.health_score import HealthScoreCalculator
from services.industry_benchmark import IndustryBenchmark
from services.forecasting_engine import ForecastingEngine
from services.recommendation_engine import RecommendationEngine
from services.product_recommendation import ProductRecommendationEngine
from services.report_generator import ReportGenerator
from services.encryption import decrypt_data
from routers.auth import get_current_user

router = APIRouter()

def get_validated_data(company_id: int, db: Session):
    """Get validated financial data for a company"""
    data = db.query(FinancialData).filter(
        FinancialData.company_id == company_id,
        FinancialData.is_validated == True
    ).order_by(FinancialData.validated_at.desc()).first()
    return data

def parse_financial_data(encrypted_data: str) -> dict:
    """Decrypt and parse financial data"""
    try:
        decrypted = decrypt_data(encrypted_data)
        return json.loads(decrypted)
    except:
        return {}

@router.get("/health-score/{company_id}")
async def get_health_score(
    company_id: int,
    recalculate: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get financial health score for a company"""
    # Verify ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Check for cached score
    if not recalculate:
        cached = db.query(HealthScore).filter(
            HealthScore.company_id == company_id
        ).order_by(HealthScore.calculated_at.desc()).first()
        
        if cached:
            return {
                "overall_score": cached.overall_score,
                "score_grade": cached.score_grade,
                "risk_level": cached.risk_level,
                "liquidity_score": cached.liquidity_score,
                "profitability_score": cached.profitability_score,
                "solvency_score": cached.solvency_score,
                "efficiency_score": cached.efficiency_score,
                "cash_flow_score": cached.cash_flow_score,
                "industry_percentile": cached.industry_percentile,
                "summary": cached.summary,
                "risk_factors": json.loads(cached.risk_factors) if cached.risk_factors else [],
                "recommendations": json.loads(cached.recommendations) if cached.recommendations else [],
                "benchmark_data": json.loads(cached.benchmark_data) if cached.benchmark_data else {},
                "forecast_data": json.loads(cached.forecast_data) if cached.forecast_data else {},
                "metrics": json.loads(cached.metrics) if cached.metrics else {}
            }
    
    # Get validated financial data
    financial_data = get_validated_data(company_id, db)
    if not financial_data:
        raise HTTPException(
            status_code=404, 
            detail="No validated financial data found. Please upload and validate your documents."
        )
    
    # Parse data
    data = parse_financial_data(financial_data.encrypted_data)
    if not data:
        raise HTTPException(status_code=500, detail="Failed to parse financial data")
    
    # Calculate scores
    calculator = HealthScoreCalculator(company.industry)
    score_result = calculator.calculate_comprehensive_score(data)
    
    # Get benchmarks
    benchmark = IndustryBenchmark()
    benchmark_data = benchmark.compare_to_industry(score_result.get("metrics", {}), company.industry)
    
    # Generate forecast
    forecaster = ForecastingEngine()
    forecast_data = forecaster.generate_forecast(data, company.industry)
    
    # Generate recommendations
    recommender = RecommendationEngine()
    recommendations = recommender.get_recommendations(
        score_result.get("overall_score", 50),
        score_result.get("metrics", {}),
        company.industry
    )
    
    # Store in database
    health_score = HealthScore(
        company_id=company_id,
        overall_score=score_result["overall_score"],
        score_grade=score_result["grade"],
        risk_level=score_result["risk_level"],
        liquidity_score=score_result.get("liquidity_score", 50),
        profitability_score=score_result.get("profitability_score", 50),
        solvency_score=score_result.get("solvency_score", 50),
        efficiency_score=score_result.get("efficiency_score", 50),
        cash_flow_score=score_result.get("cash_flow_score", 50),
        industry_percentile=benchmark_data.get("summary", {}).get("overall_percentile", 50),
        summary=score_result.get("ai_summary", ""),
        risk_factors=json.dumps(score_result.get("risk_factors", [])),
        recommendations=json.dumps(recommendations),
        benchmark_data=json.dumps(benchmark_data),
        forecast_data=json.dumps(forecast_data),
        metrics=json.dumps(score_result.get("metrics", {}))
    )
    
    db.add(health_score)
    db.commit()
    
    return {
        "overall_score": score_result["overall_score"],
        "score_grade": score_result["grade"],
        "risk_level": score_result["risk_level"],
        "liquidity_score": score_result.get("liquidity_score", 50),
        "profitability_score": score_result.get("profitability_score", 50),
        "solvency_score": score_result.get("solvency_score", 50),
        "efficiency_score": score_result.get("efficiency_score", 50),
        "cash_flow_score": score_result.get("cash_flow_score", 50),
        "industry_percentile": benchmark_data.get("summary", {}).get("overall_percentile", 50),
        "summary": score_result.get("ai_summary", ""),
        "risk_factors": score_result.get("risk_factors", []),
        "recommendations": recommendations,
        "benchmark_data": benchmark_data,
        "forecast_data": forecast_data,
        "metrics": score_result.get("metrics", {})
    }

@router.get("/summary/{company_id}")
async def get_summary(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a quick summary of financial health"""
    # Verify ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get latest health score
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    if not health_score:
        return {
            "has_data": False,
            "message": "No analysis available. Upload and validate financial documents to get started."
        }
    
    return {
        "has_data": True,
        "overall_score": health_score.overall_score,
        "grade": health_score.score_grade,
        "risk_level": health_score.risk_level,
        "industry_percentile": health_score.industry_percentile,
        "summary": health_score.summary,
        "last_updated": health_score.calculated_at
    }

@router.get("/benchmark/{company_id}")
async def get_benchmark(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get industry benchmark comparison"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    if not health_score or not health_score.benchmark_data:
        raise HTTPException(status_code=404, detail="No benchmark data available")
    
    return json.loads(health_score.benchmark_data)

@router.get("/forecast/{company_id}")
async def get_forecast(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get financial forecast"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    if not health_score or not health_score.forecast_data:
        raise HTTPException(status_code=404, detail="No forecast data available")
    
    return json.loads(health_score.forecast_data)


@router.get("/products/{company_id}")
async def get_product_recommendations(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized financial product recommendations"""
    # Verify ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get latest health score
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    if not health_score:
        # Return generic recommendations for new companies
        engine = ProductRecommendationEngine()
        return {
            "has_analysis": False,
            "message": "Upload financial data for personalized recommendations",
            "available_products": engine.get_all_products()[:5]
        }
    
    # Get metrics
    metrics = json.loads(health_score.metrics) if health_score.metrics else {}
    
    # Generate personalized recommendations
    engine = ProductRecommendationEngine()
    recommendations = engine.get_recommendations(
        health_score=health_score.overall_score,
        metrics=metrics,
        industry=company.industry,
        company_age_years=2  # TODO: Add company age to model
    )
    
    return {
        "has_analysis": True,
        "health_score": health_score.overall_score,
        "risk_level": health_score.risk_level,
        **recommendations
    }


@router.get("/products")
async def get_all_products(
    current_user: User = Depends(get_current_user)
):
    """Get all available financial products"""
    engine = ProductRecommendationEngine()
    return {
        "products": engine.get_all_products(),
        "total": len(engine.get_all_products())
    }


@router.get("/report/{company_id}")
async def download_report(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate and download investor-ready PDF report"""
    # Verify ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get latest health score
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    if not health_score:
        raise HTTPException(
            status_code=404, 
            detail="No analysis available. Please upload financial data first."
        )
    
    # Build health score data
    score_data = {
        "overall_score": health_score.overall_score,
        "score_grade": health_score.score_grade,
        "risk_level": health_score.risk_level,
        "liquidity_score": health_score.liquidity_score,
        "profitability_score": health_score.profitability_score,
        "solvency_score": health_score.solvency_score,
        "efficiency_score": health_score.efficiency_score,
        "cash_flow_score": health_score.cash_flow_score,
        "summary": health_score.summary,
        "risk_factors": json.loads(health_score.risk_factors) if health_score.risk_factors else [],
        "recommendations": json.loads(health_score.recommendations) if health_score.recommendations else [],
        "metrics": json.loads(health_score.metrics) if health_score.metrics else {},
        "forecast_data": json.loads(health_score.forecast_data) if health_score.forecast_data else {}
    }
    
    # Get product recommendations
    metrics = json.loads(health_score.metrics) if health_score.metrics else {}
    product_engine = ProductRecommendationEngine()
    product_recs = product_engine.get_recommendations(
        health_score=health_score.overall_score,
        metrics=metrics,
        industry=company.industry
    )
    
    top_products = (
        product_recs.get('highly_recommended', []) + 
        product_recs.get('good_options', [])
    )[:3]
    
    # Generate PDF
    generator = ReportGenerator()
    pdf_buffer = generator.generate_health_report(
        company_name=company.name,
        industry=company.industry,
        health_score=score_data,
        product_recommendations=top_products
    )
    
    # Return as downloadable file
    filename = f"{company.name.replace(' ', '_')}_Financial_Health_Report.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


# ============================================
# NEW: Competition-Winning Features
# ============================================

from services.business_insights import BusinessInsightsService


@router.get("/risk-alerts/{company_id}")
async def get_risk_alerts(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get smart risk alerts for a company - CFO-style warnings"""
    # Verify ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get latest health score
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    if not health_score:
        return {
            "has_data": False,
            "alerts": [],
            "message": "Upload financial data to see risk alerts"
        }
    
    # Build health score dict
    score_data = {
        "overall_score": health_score.overall_score,
        "metrics": json.loads(health_score.metrics) if health_score.metrics else {},
        "risk_factors": json.loads(health_score.risk_factors) if health_score.risk_factors else []
    }
    
    # Generate alerts
    insights_service = BusinessInsightsService()
    alerts = insights_service.get_risk_alerts(score_data)
    
    return {
        "has_data": True,
        "company_name": company.name,
        "overall_score": health_score.overall_score,
        "alerts": alerts,
        "total_alerts": len(alerts),
        "critical_count": len([a for a in alerts if a['type'] == 'critical']),
        "warning_count": len([a for a in alerts if a['type'] == 'warning'])
    }


@router.get("/cfo-insights/{company_id}")
async def get_cfo_insights(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get CFO-style business insights - human-readable interpretations"""
    # Verify ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get latest health score
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    if not health_score:
        return {
            "has_data": False,
            "insights": [],
            "message": "Upload financial data to see CFO insights"
        }
    
    # Build health score dict
    score_data = {
        "overall_score": health_score.overall_score,
        "metrics": json.loads(health_score.metrics) if health_score.metrics else {},
        "risk_factors": json.loads(health_score.risk_factors) if health_score.risk_factors else []
    }
    
    # Generate insights
    insights_service = BusinessInsightsService()
    insights = insights_service.get_cfo_insights(score_data, company.industry)
    
    return {
        "has_data": True,
        "company_name": company.name,
        "industry": company.industry,
        "insights": insights
    }


@router.get("/action-plan/{company_id}")
async def get_action_plan(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a 90-day financial action plan using AI"""
    # Verify ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get latest health score
    health_score = db.query(HealthScore).filter(
        HealthScore.company_id == company_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    if not health_score:
        return {
            "has_data": False,
            "plan": None,
            "message": "Upload financial data to generate an action plan"
        }
    
    # Build health score dict
    score_data = {
        "overall_score": health_score.overall_score,
        "metrics": json.loads(health_score.metrics) if health_score.metrics else {},
        "risk_factors": json.loads(health_score.risk_factors) if health_score.risk_factors else []
    }
    
    # Generate action plan
    insights_service = BusinessInsightsService()
    action_plan = await insights_service.generate_action_plan(
        score_data, 
        company.name, 
        company.industry
    )
    
    return {
        "has_data": True,
        "company_name": company.name,
        "plan": action_plan
    }

