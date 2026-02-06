# Financial Calculator - Core financial metrics computation
from typing import Dict, Any, Optional
import math

class FinancialCalculator:
    """Calculate financial ratios and metrics using Python (not LLM)"""
    
    def calculate_all_metrics(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate all financial metrics from raw data"""
        # Extract key financial values
        financials = self._extract_financials(raw_data)
        
        metrics = {
            # Liquidity Ratios
            "current_ratio": self._safe_divide(
                financials.get("current_assets", 0),
                financials.get("current_liabilities", 1)
            ),
            "quick_ratio": self._safe_divide(
                financials.get("current_assets", 0) - financials.get("inventory", 0),
                financials.get("current_liabilities", 1)
            ),
            "cash_ratio": self._safe_divide(
                financials.get("cash", 0),
                financials.get("current_liabilities", 1)
            ),
            
            # Profitability Ratios
            "gross_margin": self._safe_divide(
                financials.get("gross_profit", 0),
                financials.get("revenue", 1)
            ) * 100,
            "net_margin": self._safe_divide(
                financials.get("net_profit", 0),
                financials.get("revenue", 1)
            ) * 100,
            "operating_margin": self._safe_divide(
                financials.get("operating_income", 0),
                financials.get("revenue", 1)
            ) * 100,
            "roe": self._safe_divide(
                financials.get("net_profit", 0),
                financials.get("equity", 1)
            ) * 100,
            "roa": self._safe_divide(
                financials.get("net_profit", 0),
                financials.get("total_assets", 1)
            ) * 100,
            
            # Solvency Ratios
            "debt_to_equity": self._safe_divide(
                financials.get("total_debt", 0),
                financials.get("equity", 1)
            ),
            "debt_ratio": self._safe_divide(
                financials.get("total_debt", 0),
                financials.get("total_assets", 1)
            ),
            "interest_coverage": self._safe_divide(
                financials.get("operating_income", 0),
                financials.get("interest_expense", 1)
            ),
            
            # Efficiency Ratios
            "inventory_turnover": self._safe_divide(
                financials.get("cost_of_goods_sold", 0),
                financials.get("inventory", 1)
            ),
            "receivables_turnover": self._safe_divide(
                financials.get("revenue", 0),
                financials.get("accounts_receivable", 1)
            ),
            "payables_turnover": self._safe_divide(
                financials.get("cost_of_goods_sold", 0),
                financials.get("accounts_payable", 1)
            ),
            "asset_turnover": self._safe_divide(
                financials.get("revenue", 0),
                financials.get("total_assets", 1)
            ),
            
            # Cash Flow Metrics
            "cash_runway_days": self._calculate_cash_runway(financials),
            "working_capital": (
                financials.get("current_assets", 0) - 
                financials.get("current_liabilities", 0)
            ),
            "working_capital_cycle": self._calculate_working_capital_cycle(financials),
            
            # Growth Metrics (if historical data available)
            "revenue_growth": financials.get("revenue_growth", None),
            "profit_growth": financials.get("profit_growth", None),
            
            # Raw Values (for context)
            "raw_values": {
                "revenue": financials.get("revenue", 0),
                "expenses": financials.get("total_expenses", 0),
                "net_profit": financials.get("net_profit", 0),
                "cash": financials.get("cash", 0),
                "total_assets": financials.get("total_assets", 0),
                "total_liabilities": financials.get("total_liabilities", 0)
            }
        }
        
        return metrics
    
    def _extract_financials(self, raw_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract financial values from raw data structure"""
        financials = {}
        
        # Check if data has summary or financial_data
        if "summary" in raw_data:
            summary = raw_data["summary"]
            financials.update({
                "revenue": summary.get("total_revenue", 0),
                "total_expenses": summary.get("total_expenses", 0),
                "net_profit": summary.get("total_profit", 0),
                "total_assets": summary.get("total_assets", 0),
                "total_liabilities": summary.get("total_liabilities", 0)
            })
        
        if "financial_data" in raw_data:
            for col, info in raw_data["financial_data"].items():
                category = info.get("category", "")
                total = info.get("total", 0)
                
                if category == "revenue":
                    financials["revenue"] = financials.get("revenue", 0) + total
                elif category == "expense":
                    financials["total_expenses"] = financials.get("total_expenses", 0) + total
                elif category == "profit":
                    financials["net_profit"] = total
                elif category == "asset":
                    financials["total_assets"] = financials.get("total_assets", 0) + total
                    # Check specific asset types
                    col_lower = col.lower()
                    if "cash" in col_lower or "bank" in col_lower:
                        financials["cash"] = financials.get("cash", 0) + total
                    elif "inventory" in col_lower:
                        financials["inventory"] = financials.get("inventory", 0) + total
                    elif "receivable" in col_lower:
                        financials["accounts_receivable"] = financials.get("accounts_receivable", 0) + total
                elif category == "liability":
                    financials["total_liabilities"] = financials.get("total_liabilities", 0) + total
                    if "payable" in col.lower():
                        financials["accounts_payable"] = financials.get("accounts_payable", 0) + total
        
        # Calculate derived values
        if "revenue" in financials and "total_expenses" in financials:
            if "net_profit" not in financials:
                financials["net_profit"] = financials["revenue"] - financials["total_expenses"]
            financials["gross_profit"] = financials["revenue"] * 0.35  # Estimate if not available
            financials["operating_income"] = financials["net_profit"] * 1.2  # Estimate
        
        # Set default current assets/liabilities
        financials["current_assets"] = financials.get("cash", 0) + \
                                       financials.get("accounts_receivable", 0) + \
                                       financials.get("inventory", 0)
        financials["current_liabilities"] = financials.get("accounts_payable", 0) + \
                                            financials.get("total_liabilities", 0) * 0.3
        
        # Equity calculation
        financials["equity"] = financials.get("total_assets", 0) - financials.get("total_liabilities", 0)
        financials["total_debt"] = financials.get("total_liabilities", 0)
        financials["cost_of_goods_sold"] = financials.get("total_expenses", 0) * 0.7
        
        return financials
    
    def _safe_divide(self, numerator: float, denominator: float) -> float:
        """Safe division that handles zero denominator"""
        if denominator == 0:
            return 0.0
        return numerator / denominator
    
    def _calculate_cash_runway(self, financials: Dict[str, float]) -> float:
        """Calculate cash runway in days"""
        cash = financials.get("cash", 0)
        monthly_expenses = financials.get("total_expenses", 0) / 12
        
        if monthly_expenses <= 0:
            return 365  # Default to 1 year if no expenses
        
        daily_burn = monthly_expenses / 30
        return round(cash / daily_burn) if daily_burn > 0 else 365
    
    def _calculate_working_capital_cycle(self, financials: Dict[str, float]) -> float:
        """Calculate working capital cycle in days"""
        # Days Inventory Outstanding
        inventory = financials.get("inventory", 0)
        cogs = financials.get("cost_of_goods_sold", 1)
        dio = (inventory / cogs) * 365 if cogs > 0 else 0
        
        # Days Sales Outstanding
        receivables = financials.get("accounts_receivable", 0)
        revenue = financials.get("revenue", 1)
        dso = (receivables / revenue) * 365 if revenue > 0 else 0
        
        # Days Payable Outstanding
        payables = financials.get("accounts_payable", 0)
        dpo = (payables / cogs) * 365 if cogs > 0 else 0
        
        # Working Capital Cycle = DIO + DSO - DPO
        return round(dio + dso - dpo)
