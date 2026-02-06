"""
Upload Router - File upload and human-in-the-loop validation
"""
import json
from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
import io

from database import get_db
from models import User, Company, FinancialData
from services.encryption import encrypt_data
from routers.auth import get_current_user

# Helper function to recursively clean data for JSON serialization
def _clean_for_json(obj):
    """Recursively clean data to be JSON-serializable."""
    if obj is None:
        return None
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return float(obj)
    if isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return obj
    if isinstance(obj, np.ndarray):
        return [_clean_for_json(item) for item in obj.tolist()]
    if isinstance(obj, dict):
        return {str(k): _clean_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean_for_json(item) for item in obj]
    if pd.isna(obj):
        return None
    # Handle pandas Timestamp
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    # Fallback for any other types
    try:
        json.dumps(obj)  # Test if serializable
        return obj
    except (TypeError, ValueError):
        return str(obj)

def safe_json_dumps(data):
    """Safely serialize data to JSON, handling NaN, Infinity, datetime, etc."""
    cleaned = _clean_for_json(data)
    return json.dumps(cleaned)

router = APIRouter()

# Schemas
class CompanyCreate(BaseModel):
    name: str
    industry: str

class CompanyResponse(BaseModel):
    id: int
    name: str
    industry: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ValidationRequest(BaseModel):
    financial_data_id: int
    is_approved: bool

class FinancialDataResponse(BaseModel):
    id: int
    company_id: int
    file_name: str
    upload_date: datetime
    is_validated: bool
    preview_data: Optional[dict] = None
    
    class Config:
        from_attributes = True

# Endpoints
@router.post("/company", response_model=CompanyResponse)
async def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new company for the current user"""
    # Check for duplicate company name for this user
    existing = db.query(Company).filter(
        Company.user_id == current_user.id,
        Company.name == company_data.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Company with name '{company_data.name}' already exists"
        )
    
    company = Company(
        user_id=current_user.id,
        name=company_data.name,
        industry=company_data.industry
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@router.get("/companies", response_model=List[CompanyResponse])
async def get_companies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all companies for the current user"""
    return db.query(Company).filter(Company.user_id == current_user.id).all()

@router.get("/company/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific company"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.delete("/company/{company_id}")
async def delete_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a company and all its associated data"""
    # Verify company ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company_name = company.name
    
    # Delete associated financial data
    db.query(FinancialData).filter(FinancialData.company_id == company_id).delete()
    
    # Delete associated health scores
    from models import HealthScore
    db.query(HealthScore).filter(HealthScore.company_id == company_id).delete()
    
    # Delete the company
    db.delete(company)
    db.commit()
    
    return {"message": f"Company '{company_name}' and all associated data deleted successfully"}

@router.post("/file/{company_id}")
async def upload_file(
    company_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a financial document (CSV, XLSX, or PDF)"""
    # Verify company ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Validate file type
    filename = file.filename.lower()
    supported_formats = ['.csv', '.xlsx', '.xls', '.pdf']
    
    if not any(filename.endswith(ext) for ext in supported_formats):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Supported formats: CSV, XLSX, PDF"
        )
    
    # Read file
    content = await file.read()
    
    try:
        preview_data = {}
        data_json = ""
        
        # Parse based on file type
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
            preview_data = {
                "columns": df.columns.tolist(),
                "row_count": len(df),
                "preview": df.head(5).to_dict(orient="records"),
                "detected_categories": detect_financial_categories(df)
            }
            data_json = df.to_json()
            
        elif filename.endswith(('.xlsx', '.xls')):
            # Read all sheets from Excel file
            all_sheets = pd.read_excel(io.BytesIO(content), sheet_name=None)
            
            # Combine all sheets with data
            combined_df = pd.DataFrame()
            sheets_info = []
            
            for sheet_name, sheet_df in all_sheets.items():
                if len(sheet_df) > 0 and len(sheet_df.columns) > 0:
                    # Add sheet name as identifier
                    sheet_df = sheet_df.copy()
                    sheet_df['_sheet_name'] = sheet_name
                    combined_df = pd.concat([combined_df, sheet_df], ignore_index=True)
                    sheets_info.append({
                        "name": sheet_name,
                        "rows": len(sheet_df),
                        "columns": len(sheet_df.columns)
                    })
            
            # If no data found, try first sheet anyway
            if len(combined_df) == 0:
                first_sheet_name = list(all_sheets.keys())[0] if all_sheets else "Sheet1"
                combined_df = all_sheets.get(first_sheet_name, pd.DataFrame())
            
            # Clean column names
            combined_df.columns = combined_df.columns.astype(str)
            
            # Replace NaN, Infinity values with None for JSON compatibility
            combined_df = combined_df.replace([np.inf, -np.inf], None)
            combined_df = combined_df.where(pd.notnull(combined_df), None)
            
            # Get preview with cleaned data
            preview_df = combined_df.head(5).copy()
            preview_records = []
            for _, row in preview_df.iterrows():
                record = {}
                for col in row.index:
                    val = row[col]
                    if pd.isna(val) or (isinstance(val, float) and (np.isinf(val) or np.isnan(val))):
                        record[col] = None
                    else:
                        record[col] = val
                preview_records.append(record)
            
            preview_data = {
                "columns": combined_df.columns.tolist()[:20],  # Limit columns shown
                "row_count": len(combined_df),
                "sheet_count": len(all_sheets),
                "sheets": sheets_info[:10],  # Show up to 10 sheets
                "preview": preview_records,
                "detected_categories": detect_financial_categories(combined_df)
            }
            # Use orient='records' with default handler for JSON serialization
            data_json = combined_df.to_json(default_handler=str)
            
        elif filename.endswith('.pdf'):
            # Handle PDF using FileProcessor
            from services.file_processor import FileProcessor
            import tempfile
            import os
            
            # Save PDF temporarily for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            try:
                processor = FileProcessor()
                pdf_result = processor.process_file(tmp_path, 'pdf')
                
                preview_data = {
                    "file_type": "pdf",
                    "page_count": pdf_result.get("page_count", 0),
                    "tables_found": pdf_result.get("tables_found", 0),
                    "text_preview": pdf_result.get("text_preview", "")[:500],
                    "detected_categories": list(pdf_result.get("financial_data", {}).keys()),
                    "financial_data": pdf_result.get("financial_data", {})
                }
                data_json = safe_json_dumps(pdf_result)
            finally:
                # Clean up temp file
                os.unlink(tmp_path)
        
        # Encrypt and store
        encrypted_content = encrypt_data(data_json)
        
        financial_data = FinancialData(
            company_id=company_id,
            file_name=file.filename,
            encrypted_data=encrypted_content,
            is_validated=False,  # Requires human validation
            preview_data=safe_json_dumps(preview_data)
        )
        
        db.add(financial_data)
        db.commit()
        db.refresh(financial_data)
        
        return {
            "message": "File uploaded successfully. Please review and validate the data.",
            "file_id": financial_data.id,
            "file_type": "pdf" if filename.endswith('.pdf') else "spreadsheet",
            "preview_data": preview_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

def detect_financial_categories(df: pd.DataFrame) -> List[str]:
    """Detect which financial categories are present in the data"""
    categories = []
    columns_lower = [col.lower() for col in df.columns]
    
    # Check for revenue/sales data
    if any(term in ' '.join(columns_lower) for term in ['revenue', 'sales', 'income']):
        categories.append("Revenue/Sales Data")
    
    # Check for expense data
    if any(term in ' '.join(columns_lower) for term in ['expense', 'cost', 'spending']):
        categories.append("Expense Data")
    
    # Check for balance sheet items
    if any(term in ' '.join(columns_lower) for term in ['asset', 'liability', 'equity', 'balance']):
        categories.append("Balance Sheet Data")
    
    # Check for cash flow
    if any(term in ' '.join(columns_lower) for term in ['cash', 'flow', 'payment', 'receivable']):
        categories.append("Cash Flow Data")
    
    # Check for dates
    if any(term in ' '.join(columns_lower) for term in ['date', 'period', 'month', 'year']):
        categories.append("Time Series Data")
    
    return categories if categories else ["General Financial Data"]

@router.get("/pending/{company_id}", response_model=List[FinancialDataResponse])
async def get_pending_validations(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all pending validations for a company"""
    # Verify company ownership
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    pending = db.query(FinancialData).filter(
        FinancialData.company_id == company_id,
        FinancialData.is_validated == False
    ).all()
    
    # Parse preview_data JSON for each
    for item in pending:
        if item.preview_data:
            item.preview_data = json.loads(item.preview_data)
    
    return pending

@router.post("/validate")
async def validate_data(
    request: ValidationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Validate or reject uploaded financial data (Human-in-the-Loop)"""
    # Find the financial data
    financial_data = db.query(FinancialData).filter(
        FinancialData.id == request.financial_data_id
    ).first()
    
    if not financial_data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    # Verify ownership through company
    company = db.query(Company).filter(
        Company.id == financial_data.company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if request.is_approved:
        financial_data.is_validated = True
        financial_data.validated_at = datetime.utcnow()
        db.commit()
        return {"message": "Data validated successfully", "status": "approved"}
    else:
        # Delete rejected data
        db.delete(financial_data)
        db.commit()
        return {"message": "Data rejected and removed", "status": "rejected"}
