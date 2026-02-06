"""
SQLAlchemy Database Models for SME Financial Health Platform
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    preferred_language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    companies = relationship("Company", back_populates="owner")


class Company(Base):
    """Company model representing an SME"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=False)  # Manufacturing, Retail, Agriculture, Services, Logistics, E-commerce
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="companies")
    financial_data = relationship("FinancialData", back_populates="company")
    health_scores = relationship("HealthScore", back_populates="company")


class FinancialData(Base):
    """Encrypted financial data storage"""
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    encrypted_data = Column(LargeBinary, nullable=False)  # AES-256 encrypted
    upload_date = Column(DateTime, default=datetime.utcnow)
    is_validated = Column(Boolean, default=False)  # Human-in-the-loop validation
    validated_at = Column(DateTime, nullable=True)
    preview_data = Column(Text, nullable=True)  # JSON preview for validation UI
    
    # Relationships
    company = relationship("Company", back_populates="financial_data")


class HealthScore(Base):
    """Calculated health scores and analysis results"""
    __tablename__ = "health_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Core scores
    overall_score = Column(Float, nullable=False)  # 0-100
    score_grade = Column(String(2), nullable=False)  # A+, A, B+, B, C+, C, D, F
    risk_level = Column(String(20), nullable=False)  # Low, Medium, High, Critical
    
    # Component scores
    liquidity_score = Column(Float, default=50)
    profitability_score = Column(Float, default=50)
    solvency_score = Column(Float, default=50)
    efficiency_score = Column(Float, default=50)
    cash_flow_score = Column(Float, default=50)
    
    # Benchmarking
    industry_percentile = Column(Float, nullable=True)  # Compared to industry
    
    # AI-generated content (JSON strings)
    summary = Column(Text, nullable=True)  # AI-generated explanation
    risk_factors = Column(Text, nullable=True)  # JSON array of risks
    recommendations = Column(Text, nullable=True)  # JSON array of recommendations
    benchmark_data = Column(Text, nullable=True)  # JSON benchmark comparison
    forecast_data = Column(Text, nullable=True)  # JSON forecast data
    metrics = Column(Text, nullable=True)  # JSON detailed metrics
    
    # Relationships
    company = relationship("Company", back_populates="health_scores")
