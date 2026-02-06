# File Processor - Handles CSV, XLSX, PDF parsing
import pandas as pd
from typing import Dict, Any, List
import os

class FileProcessor:
    """Process uploaded financial documents and extract structured data"""
    
    def __init__(self):
        self.supported_formats = ["csv", "xlsx", "pdf"]
    
    def process_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Process file and return structured data summary"""
        if file_type == "csv":
            return self._process_csv(file_path)
        elif file_type == "xlsx":
            return self._process_xlsx(file_path)
        elif file_type == "pdf":
            return self._process_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _process_csv(self, file_path: str) -> Dict[str, Any]:
        """Process CSV file"""
        df = pd.read_csv(file_path)
        return self._extract_financial_summary(df)
    
    def _process_xlsx(self, file_path: str) -> Dict[str, Any]:
        """Process Excel file"""
        # Try to read all sheets
        xlsx = pd.ExcelFile(file_path)
        all_data = {}
        
        for sheet_name in xlsx.sheet_names:
            df = pd.read_excel(xlsx, sheet_name=sheet_name)
            all_data[sheet_name] = self._extract_financial_summary(df)
        
        # Combine sheets if multiple
        if len(all_data) == 1:
            return list(all_data.values())[0]
        
        return {
            "sheets": all_data,
            "summary": self._combine_sheet_summaries(all_data)
        }
    
    def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """Process PDF file using PyMuPDF and convert to standardized JSON"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            return {
                "status": "pdf_processing_unavailable",
                "message": "PDF processing library not installed. Please upload CSV or XLSX files.",
                "file_name": os.path.basename(file_path)
            }
        
        try:
            doc = fitz.open(file_path)
            full_text = []
            tables_data = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                full_text.append(text)
                
                # Try to extract tables from the page
                tables = page.find_tables()
                if tables:
                    for table in tables:
                        table_data = table.extract()
                        if table_data and len(table_data) > 0:
                            tables_data.append({
                                "page": page_num + 1,
                                "data": table_data
                            })
            
            doc.close()
            
            # Combine text and extract financial data
            combined_text = "\n".join(full_text)
            
            # Extract raw financial values from text
            raw_financial = self._extract_financial_from_text(combined_text)
            
            # Convert to standardized JSON format for health score calculation
            standardized_data = self._convert_to_standardized_json(raw_financial, tables_data)
            
            return {
                "status": "success",
                "file_name": os.path.basename(file_path),
                "page_count": len(full_text),
                "text_preview": combined_text[:2000],
                "tables_found": len(tables_data),
                **standardized_data
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to process PDF: {str(e)}",
                "file_name": os.path.basename(file_path)
            }
    
    def _extract_financial_from_text(self, text: str) -> Dict[str, float]:
        """Extract financial values from text using regex patterns"""
        import re
        
        financial_data = {}
        
        # Common patterns for Indian currency format
        patterns = {
            "revenue": r"(?:revenue|sales|total income|turnover)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "profit": r"(?:net profit|profit after tax|pat|net income)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "gross_profit": r"(?:gross profit)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "expenses": r"(?:total expense|operating expense|expenditure)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "cash": r"(?:cash and bank|cash balance|cash in hand)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "total_assets": r"(?:total assets)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "current_assets": r"(?:current assets)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "total_liabilities": r"(?:total liabilities)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "current_liabilities": r"(?:current liabilities)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "equity": r"(?:total equity|shareholder equity|net worth)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "inventory": r"(?:inventory|stock)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "receivables": r"(?:receivable|debtors)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "payables": r"(?:payable|creditors)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
            "debt": r"(?:total debt|long term debt|borrowings)[^0-9]*[₹Rs.\s]*([0-9,]+(?:\.[0-9]+)?)",
        }
        
        text_lower = text.lower()
        
        for category, pattern in patterns.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                # Clean and take the largest value (usually annual figures)
                values = []
                for match in matches:
                    try:
                        clean_val = match.replace(",", "").strip()
                        if clean_val:
                            values.append(float(clean_val))
                    except:
                        pass
                
                if values:
                    financial_data[category] = max(values)
        
        return financial_data
    
    def _convert_to_standardized_json(self, raw_data: Dict[str, float], tables: List) -> Dict[str, Any]:
        """Convert extracted data to standardized JSON format for health score calculation"""
        
        # Get raw values with defaults
        revenue = raw_data.get("revenue", 1000000)  # Default ₹10L
        profit = raw_data.get("profit", revenue * 0.1)  # Default 10% margin
        gross_profit = raw_data.get("gross_profit", revenue * 0.35)
        expenses = raw_data.get("expenses", revenue * 0.85)
        cash = raw_data.get("cash", 100000)
        total_assets = raw_data.get("total_assets", revenue * 0.8)
        current_assets = raw_data.get("current_assets", total_assets * 0.4)
        total_liabilities = raw_data.get("total_liabilities", total_assets * 0.4)
        current_liabilities = raw_data.get("current_liabilities", total_liabilities * 0.5)
        equity = raw_data.get("equity", total_assets - total_liabilities)
        inventory = raw_data.get("inventory", current_assets * 0.3)
        receivables = raw_data.get("receivables", current_assets * 0.4)
        debt = raw_data.get("debt", total_liabilities * 0.6)
        
        # Ensure equity is positive
        if equity <= 0:
            equity = total_assets * 0.3
        
        # Calculate financial ratios/metrics
        current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 1.5
        quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities > 0 else 1.0
        cash_ratio = cash / current_liabilities if current_liabilities > 0 else 0.5
        
        gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 30
        net_margin = (profit / revenue * 100) if revenue > 0 else 10
        
        debt_to_equity = total_liabilities / equity if equity > 0 else 1.0
        debt_ratio = total_liabilities / total_assets if total_assets > 0 else 0.4
        
        # ROE calculation
        roe = (profit / equity * 100) if equity > 0 else 12
        
        # Estimate interest coverage (assume 15% of debt as interest)
        interest_expense = debt * 0.15
        operating_income = profit + interest_expense
        interest_coverage = operating_income / interest_expense if interest_expense > 0 else 5.0
        
        # Efficiency ratios
        inventory_turnover = (revenue * 0.65) / inventory if inventory > 0 else 6
        receivables_turnover = revenue / receivables if receivables > 0 else 8
        asset_turnover = revenue / total_assets if total_assets > 0 else 1.2
        
        # Cash flow metrics
        monthly_expenses = expenses / 12 if expenses > 0 else revenue * 0.08
        cash_runway_days = (cash / (monthly_expenses / 30)) if monthly_expenses > 0 else 90
        working_capital = current_assets - current_liabilities
        working_capital_cycle = 45  # Default estimate
        
        return {
            # Raw values for reference
            "revenue": revenue,
            "total_revenue": revenue,
            "profit": profit,
            "net_income": profit,
            "expenses": expenses,
            "cash": cash,
            "total_assets": total_assets,
            "current_assets": current_assets,
            "total_liabilities": total_liabilities,
            "current_liabilities": current_liabilities,
            "equity": equity,
            "inventory": inventory,
            "receivables": receivables,
            "debt": debt,
            
            # Calculated metrics for health score
            "current_ratio": round(min(current_ratio, 5), 2),
            "quick_ratio": round(min(quick_ratio, 4), 2),
            "cash_ratio": round(min(cash_ratio, 3), 2),
            "gross_margin": round(min(gross_margin, 80), 1),
            "net_margin": round(min(max(net_margin, -20), 40), 1),
            "roe": round(min(max(roe, -20), 50), 1),
            "debt_to_equity": round(min(debt_to_equity, 5), 2),
            "debt_ratio": round(min(debt_ratio, 1), 2),
            "interest_coverage": round(min(interest_coverage, 20), 1),
            "inventory_turnover": round(min(inventory_turnover, 30), 1),
            "receivables_turnover": round(min(receivables_turnover, 20), 1),
            "asset_turnover": round(min(asset_turnover, 5), 2),
            "cash_runway_days": round(min(cash_runway_days, 500), 0),
            "working_capital": round(working_capital, 0),
            "working_capital_cycle": working_capital_cycle,
            
            # Summary for frontend display
            "summary": {
                "total_revenue": revenue,
                "total_expenses": expenses,
                "total_profit": profit,
                "extracted_from": "pdf"
            }
        }

    
    def _extract_financial_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract financial summary from dataframe"""
        summary = {
            "columns": list(df.columns),
            "row_count": len(df),
            "preview": df.head(10).to_dict(orient="records"),
            "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "financial_data": {}
        }
        
        # Try to identify and extract financial data
        financial_keywords = {
            "revenue": ["revenue", "sales", "income", "turnover"],
            "expense": ["expense", "cost", "expenditure", "payment"],
            "profit": ["profit", "net income", "net profit", "earnings"],
            "asset": ["asset", "cash", "bank", "inventory", "receivable"],
            "liability": ["liability", "payable", "debt", "loan", "credit"],
            "equity": ["equity", "capital", "retained"]
        }
        
        # Identify columns
        for category, keywords in financial_keywords.items():
            for col in df.columns:
                col_lower = str(col).lower()
                if any(kw in col_lower for kw in keywords):
                    # Extract numeric values
                    if pd.api.types.is_numeric_dtype(df[col]):
                        summary["financial_data"][col] = {
                            "category": category,
                            "total": float(df[col].sum()),
                            "mean": float(df[col].mean()),
                            "count": int(df[col].count())
                        }
        
        # Calculate totals if identifiable
        summary["detected_categories"] = list(set(
            v["category"] for v in summary["financial_data"].values()
        ))
        
        # Extract date column if present
        for col in df.columns:
            if any(d in str(col).lower() for d in ["date", "period", "month", "year"]):
                try:
                    dates = pd.to_datetime(df[col], errors='coerce')
                    valid_dates = dates.dropna()
                    if len(valid_dates) > 0:
                        summary["date_range"] = {
                            "start": str(valid_dates.min()),
                            "end": str(valid_dates.max())
                        }
                        break
                except:
                    pass
        
        return summary
    
    def _combine_sheet_summaries(self, all_data: Dict[str, Dict]) -> Dict[str, Any]:
        """Combine summaries from multiple sheets"""
        combined = {
            "total_revenue": 0,
            "total_expenses": 0,
            "total_profit": 0,
            "total_assets": 0,
            "total_liabilities": 0
        }
        
        for sheet_name, data in all_data.items():
            if "financial_data" in data:
                for col, info in data["financial_data"].items():
                    category = info.get("category", "")
                    total = info.get("total", 0)
                    
                    if category == "revenue":
                        combined["total_revenue"] += total
                    elif category == "expense":
                        combined["total_expenses"] += total
                    elif category == "profit":
                        combined["total_profit"] += total
                    elif category == "asset":
                        combined["total_assets"] += total
                    elif category == "liability":
                        combined["total_liabilities"] += total
        
        return combined
