"""
Health Score Calculator - Wrapper for health score engine
"""
from typing import Dict, Any
from .health_score_engine import HealthScoreEngine


class HealthScoreCalculator(HealthScoreEngine):
    """Health Score Calculator with industry-specific calculations"""
    
    def __init__(self, industry: str = "Services"):
        """Initialize with industry for industry-specific weights"""
        self.industry = industry
    
    def calculate_comprehensive_score(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive health score from raw financial data"""
        
        # Extract or calculate metrics from raw financial data
        metrics = self._extract_metrics(financial_data)
        
        # Calculate health score using parent class
        score_result = self.calculate_health_score(metrics, self.industry)
        
        # Add extracted metrics to result
        score_result["metrics"] = metrics
        
        # Generate AI summary
        score_result["ai_summary"] = self._generate_summary(score_result)
        
        # Identify risk factors
        score_result["risk_factors"] = self._identify_risk_factors(metrics, score_result)
        
        return score_result
    
    def _extract_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract financial metrics from raw data"""
        metrics = {}
        
        # Try to extract from structured data
        if isinstance(data, dict):
            # Direct metric fields (if already calculated)
            metrics["current_ratio"] = float(data.get("current_ratio", 1.5))
            metrics["quick_ratio"] = float(data.get("quick_ratio", 1.0))
            metrics["cash_ratio"] = float(data.get("cash_ratio", 0.5))
            metrics["gross_margin"] = float(data.get("gross_margin", 30))
            metrics["net_margin"] = float(data.get("net_margin", 10))
            metrics["roe"] = float(data.get("roe", 12))
            metrics["debt_to_equity"] = float(data.get("debt_to_equity", 0.8))
            metrics["debt_ratio"] = float(data.get("debt_ratio", 0.4))
            metrics["interest_coverage"] = float(data.get("interest_coverage", 3.0))
            metrics["inventory_turnover"] = float(data.get("inventory_turnover", 6))
            metrics["receivables_turnover"] = float(data.get("receivables_turnover", 8))
            metrics["asset_turnover"] = float(data.get("asset_turnover", 1.2))
            metrics["cash_runway_days"] = float(data.get("cash_runway_days", 90))
            metrics["working_capital"] = float(data.get("working_capital", 50000))
            metrics["working_capital_cycle"] = float(data.get("working_capital_cycle", 45))
            
            # Try to calculate metrics from raw financial statement data
            if "revenue" in data or "total_revenue" in data:
                revenue = float(data.get("revenue", data.get("total_revenue", 0)))
                cogs = float(data.get("cost_of_goods_sold", data.get("cogs", revenue * 0.6)))
                net_income = float(data.get("net_income", data.get("profit", revenue * 0.1)))
                
                if revenue > 0:
                    metrics["gross_margin"] = ((revenue - cogs) / revenue) * 100
                    metrics["net_margin"] = (net_income / revenue) * 100
            
            if "total_assets" in data or "assets" in data:
                total_assets = float(data.get("total_assets", data.get("assets", 1)))
                current_assets = float(data.get("current_assets", total_assets * 0.4))
                current_liabilities = float(data.get("current_liabilities", current_assets * 0.6))
                
                if current_liabilities > 0:
                    metrics["current_ratio"] = current_assets / current_liabilities
                
                total_liabilities = float(data.get("total_liabilities", data.get("liabilities", total_assets * 0.4)))
                equity = total_assets - total_liabilities
                
                if equity > 0:
                    metrics["debt_to_equity"] = total_liabilities / equity
                    net_income = float(data.get("net_income", data.get("profit", 0)))
                    metrics["roe"] = (net_income / equity) * 100 if equity > 0 else 0
            
            if "cash" in data or "cash_balance" in data:
                cash = float(data.get("cash", data.get("cash_balance", 0)))
                monthly_expenses = float(data.get("monthly_expenses", data.get("expenses", 0)) / 12)
                if monthly_expenses > 0:
                    metrics["cash_runway_days"] = (cash / (monthly_expenses / 30))
        
        return metrics
    
    def _generate_summary(self, score_result: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the health score"""
        score = score_result.get("overall_score", 0)
        grade = score_result.get("grade", "N/A")
        risk = score_result.get("risk_level", "Unknown")
        
        if score >= 75:
            summary = f"Your business demonstrates strong financial health with a score of {score:.0f} (Grade {grade}). "
            summary += "Key strengths include solid liquidity and healthy profitability margins. "
            summary += "Continue maintaining current financial practices and consider strategic growth investments."
        elif score >= 55:
            summary = f"Your business shows moderate financial health with a score of {score:.0f} (Grade {grade}). "
            summary += "While core fundamentals are stable, there are areas that need attention. "
            summary += "Focus on improving cash flow management and reducing debt exposure."
        elif score >= 35:
            summary = f"Your business is facing financial challenges with a score of {score:.0f} (Grade {grade}). "
            summary += "Immediate attention is required to improve liquidity and profitability. "
            summary += "Consider restructuring costs and exploring additional revenue streams."
        else:
            summary = f"Your business is in critical financial condition with a score of {score:.0f} (Grade {grade}). "
            summary += "Urgent intervention is needed to address cash flow and solvency issues. "
            summary += "Seek professional financial advice and explore emergency funding options."
        
        return summary
    
    def _identify_risk_factors(self, metrics: Dict[str, Any], score_result: Dict[str, Any]) -> list:
        """Identify key risk factors based on metrics"""
        risks = []
        
        # Liquidity risks
        if metrics.get("current_ratio", 2) < 1.0:
            risks.append({
                "name": "Low Liquidity",
                "severity": "high" if metrics.get("current_ratio", 2) < 0.8 else "medium",
                "description": "Current ratio is below 1.0, indicating potential difficulty meeting short-term obligations.",
                "indicator": f"Current Ratio: {metrics.get('current_ratio', 0):.2f}"
            })
        
        if metrics.get("cash_runway_days", 90) < 60:
            severity = "critical" if metrics.get("cash_runway_days", 90) < 30 else "high"
            risks.append({
                "name": "Low Cash Runway",
                "severity": severity,
                "description": "Cash reserves may not last beyond 2 months at current burn rate.",
                "indicator": f"Cash Runway: {metrics.get('cash_runway_days', 0):.0f} days"
            })
        
        # Profitability risks
        if metrics.get("net_margin", 10) < 5:
            risks.append({
                "name": "Low Profit Margins",
                "severity": "high" if metrics.get("net_margin", 10) < 2 else "medium",
                "description": "Net profit margin is thin, leaving little room for unexpected expenses.",
                "indicator": f"Net Margin: {metrics.get('net_margin', 0):.1f}%"
            })
        
        # Solvency risks
        if metrics.get("debt_to_equity", 1) > 2:
            risks.append({
                "name": "High Debt Levels",
                "severity": "high" if metrics.get("debt_to_equity", 1) > 3 else "medium",
                "description": "Debt-to-equity ratio is elevated, increasing financial risk.",
                "indicator": f"Debt/Equity: {metrics.get('debt_to_equity', 0):.2f}"
            })
        
        # Efficiency risks
        if metrics.get("receivables_turnover", 8) < 4:
            risks.append({
                "name": "Slow Collections",
                "severity": "medium",
                "description": "Receivables turnover is low, indicating slow collection of payments.",
                "indicator": f"Receivables Turnover: {metrics.get('receivables_turnover', 0):.1f}x"
            })
        
        return risks
