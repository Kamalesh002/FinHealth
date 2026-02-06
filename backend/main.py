"""
FastAPI Backend - Main Application Entry Point
SME Financial Health Assessment Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqladmin import Admin, ModelView

from database import engine, Base
from routers import auth as auth_router
from routers import upload as upload_router
from routers import analysis as analysis_router
from routers import chat as chat_router
from models import User, Company, FinancialData, HealthScore

# Create all database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

app = FastAPI(
    title="SME Financial Health API",
    description="AI-powered Financial Health Assessment Platform for SMEs",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(upload_router.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analysis_router.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(chat_router.router, prefix="/api/chat", tags=["Chat"])

# ============================================
# SQLAdmin - Database Browser (http://localhost:8000/admin)
# ============================================
admin = Admin(app, engine, title="SME Financial Health - Database Admin")

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.full_name, User.created_at]
    column_searchable_list = [User.email, User.full_name]
    column_sortable_list = [User.id, User.email, User.created_at]
    can_create = False  # Disable create (use API instead)
    can_delete = False  # Safety: prevent accidental deletion
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

class CompanyAdmin(ModelView, model=Company):
    column_list = [Company.id, Company.name, Company.industry, Company.user_id, Company.created_at]
    column_searchable_list = [Company.name, Company.industry]
    column_sortable_list = [Company.id, Company.name, Company.created_at]
    name = "Company"
    name_plural = "Companies"
    icon = "fa-solid fa-building"

class FinancialDataAdmin(ModelView, model=FinancialData):
    column_list = [FinancialData.id, FinancialData.company_id, FinancialData.file_name, FinancialData.upload_date, FinancialData.is_validated]
    column_sortable_list = [FinancialData.id, FinancialData.upload_date]
    name = "Financial Data"
    name_plural = "Financial Data"
    icon = "fa-solid fa-file-invoice-dollar"

class HealthScoreAdmin(ModelView, model=HealthScore):
    column_list = [HealthScore.id, HealthScore.company_id, HealthScore.overall_score, HealthScore.score_grade, HealthScore.risk_level, HealthScore.calculated_at]
    column_sortable_list = [HealthScore.id, HealthScore.overall_score, HealthScore.calculated_at]
    name = "Health Score"
    name_plural = "Health Scores"
    icon = "fa-solid fa-chart-line"

admin.add_view(UserAdmin)
admin.add_view(CompanyAdmin)
admin.add_view(FinancialDataAdmin)
admin.add_view(HealthScoreAdmin)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "SME Financial Health API"}

