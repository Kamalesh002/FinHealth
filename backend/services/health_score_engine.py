# Health Score Engine - Composite Financial Health Score
from typing import Dict, Any, Tuple

class HealthScoreEngine:
    """Calculate composite Financial Health Score (0-100)"""
    
    # Industry-specific weights
    INDUSTRY_WEIGHTS = {
        "Manufacturing": {
            "liquidity": 0.20,
            "profitability": 0.25,
            "solvency": 0.20,
            "efficiency": 0.20,
            "cash_flow": 0.15
        },
        "Retail": {
            "liquidity": 0.25,
            "profitability": 0.20,
            "solvency": 0.15,
            "efficiency": 0.25,  # Inventory turnover important
            "cash_flow": 0.15
        },
        "Agriculture": {
            "liquidity": 0.30,  # Seasonal cash needs
            "profitability": 0.20,
            "solvency": 0.15,
            "efficiency": 0.15,
            "cash_flow": 0.20
        },
        "Services": {
            "liquidity": 0.20,
            "profitability": 0.30,  # Margins matter most
            "solvency": 0.15,
            "efficiency": 0.15,
            "cash_flow": 0.20
        },
        "Logistics": {
            "liquidity": 0.20,
            "profitability": 0.20,
            "solvency": 0.25,  # Asset-heavy
            "efficiency": 0.20,
            "cash_flow": 0.15
        },
        "E-commerce": {
            "liquidity": 0.25,
            "profitability": 0.20,
            "solvency": 0.15,
            "efficiency": 0.20,
            "cash_flow": 0.20
        }
    }
    
    # Default weights
    DEFAULT_WEIGHTS = {
        "liquidity": 0.20,
        "profitability": 0.25,
        "solvency": 0.20,
        "efficiency": 0.15,
        "cash_flow": 0.20
    }
    
    def calculate_health_score(
        self, 
        metrics: Dict[str, Any], 
        industry: str
    ) -> Dict[str, Any]:
        """Calculate composite health score with component breakdown"""
        
        weights = self.INDUSTRY_WEIGHTS.get(industry, self.DEFAULT_WEIGHTS)
        
        # Calculate component scores (0-100)
        liquidity_score = self._score_liquidity(metrics)
        profitability_score = self._score_profitability(metrics)
        solvency_score = self._score_solvency(metrics)
        efficiency_score = self._score_efficiency(metrics)
        cash_flow_score = self._score_cash_flow(metrics)
        
        # Calculate weighted overall score
        overall_score = (
            liquidity_score * weights["liquidity"] +
            profitability_score * weights["profitability"] +
            solvency_score * weights["solvency"] +
            efficiency_score * weights["efficiency"] +
            cash_flow_score * weights["cash_flow"]
        )
        
        # Determine grade and risk level
        grade = self._calculate_grade(overall_score)
        risk_level = self._calculate_risk_level(overall_score)
        
        return {
            "overall_score": round(overall_score, 1),
            "grade": grade,
            "liquidity_score": round(liquidity_score, 1),
            "profitability_score": round(profitability_score, 1),
            "solvency_score": round(solvency_score, 1),
            "efficiency_score": round(efficiency_score, 1),
            "cash_flow_score": round(cash_flow_score, 1),
            "risk_level": risk_level,
            "weights_used": weights
        }
    
    def _score_liquidity(self, metrics: Dict[str, Any]) -> float:
        """Score liquidity (0-100)"""
        current_ratio = metrics.get("current_ratio", 0)
        quick_ratio = metrics.get("quick_ratio", 0)
        cash_ratio = metrics.get("cash_ratio", 0)
        
        # Current ratio scoring (ideal: 1.5-2.5)
        if current_ratio >= 2.0:
            cr_score = 100
        elif current_ratio >= 1.5:
            cr_score = 80 + (current_ratio - 1.5) * 40
        elif current_ratio >= 1.0:
            cr_score = 50 + (current_ratio - 1.0) * 60
        elif current_ratio >= 0.5:
            cr_score = 20 + (current_ratio - 0.5) * 60
        else:
            cr_score = current_ratio * 40
        
        # Quick ratio scoring (ideal: 1.0-1.5)
        if quick_ratio >= 1.5:
            qr_score = 100
        elif quick_ratio >= 1.0:
            qr_score = 70 + (quick_ratio - 1.0) * 60
        elif quick_ratio >= 0.5:
            qr_score = 30 + (quick_ratio - 0.5) * 80
        else:
            qr_score = quick_ratio * 60
        
        # Cash ratio scoring (ideal: 0.5-1.0)
        if cash_ratio >= 1.0:
            cash_score = 100
        elif cash_ratio >= 0.5:
            cash_score = 70 + (cash_ratio - 0.5) * 60
        elif cash_ratio >= 0.2:
            cash_score = 30 + (cash_ratio - 0.2) * 133
        else:
            cash_score = cash_ratio * 150
        
        return (cr_score * 0.4 + qr_score * 0.35 + cash_score * 0.25)
    
    def _score_profitability(self, metrics: Dict[str, Any]) -> float:
        """Score profitability (0-100)"""
        gross_margin = metrics.get("gross_margin", 0)
        net_margin = metrics.get("net_margin", 0)
        roe = metrics.get("roe", 0)
        
        # Gross margin scoring (ideal: 30-50%)
        if gross_margin >= 50:
            gm_score = 100
        elif gross_margin >= 30:
            gm_score = 60 + (gross_margin - 30) * 2
        elif gross_margin >= 15:
            gm_score = 30 + (gross_margin - 15) * 2
        elif gross_margin > 0:
            gm_score = gross_margin * 2
        else:
            gm_score = 0
        
        # Net margin scoring (ideal: 10-20%)
        if net_margin >= 20:
            nm_score = 100
        elif net_margin >= 10:
            nm_score = 60 + (net_margin - 10) * 4
        elif net_margin >= 5:
            nm_score = 30 + (net_margin - 5) * 6
        elif net_margin > 0:
            nm_score = net_margin * 6
        else:
            nm_score = 0
        
        # ROE scoring (ideal: 15-25%)
        if roe >= 25:
            roe_score = 100
        elif roe >= 15:
            roe_score = 60 + (roe - 15) * 4
        elif roe >= 5:
            roe_score = 20 + (roe - 5) * 4
        elif roe > 0:
            roe_score = roe * 4
        else:
            roe_score = 0
        
        return (gm_score * 0.3 + nm_score * 0.4 + roe_score * 0.3)
    
    def _score_solvency(self, metrics: Dict[str, Any]) -> float:
        """Score solvency (0-100)"""
        debt_to_equity = metrics.get("debt_to_equity", 0)
        debt_ratio = metrics.get("debt_ratio", 0)
        interest_coverage = metrics.get("interest_coverage", 0)
        
        # Debt-to-equity scoring (lower is better, ideal: < 1.0)
        if debt_to_equity <= 0.5:
            de_score = 100
        elif debt_to_equity <= 1.0:
            de_score = 70 + (1.0 - debt_to_equity) * 60
        elif debt_to_equity <= 2.0:
            de_score = 30 + (2.0 - debt_to_equity) * 40
        elif debt_to_equity <= 3.0:
            de_score = (3.0 - debt_to_equity) * 30
        else:
            de_score = 0
        
        # Debt ratio scoring (lower is better, ideal: < 0.4)
        if debt_ratio <= 0.3:
            dr_score = 100
        elif debt_ratio <= 0.5:
            dr_score = 70 + (0.5 - debt_ratio) * 150
        elif debt_ratio <= 0.7:
            dr_score = 30 + (0.7 - debt_ratio) * 200
        else:
            dr_score = max(0, (1.0 - debt_ratio) * 100)
        
        # Interest coverage scoring (higher is better, ideal: > 3)
        if interest_coverage >= 5:
            ic_score = 100
        elif interest_coverage >= 3:
            ic_score = 70 + (interest_coverage - 3) * 15
        elif interest_coverage >= 1.5:
            ic_score = 30 + (interest_coverage - 1.5) * 27
        elif interest_coverage > 1:
            ic_score = (interest_coverage - 1) * 60
        else:
            ic_score = 0
        
        return (de_score * 0.35 + dr_score * 0.35 + ic_score * 0.30)
    
    def _score_efficiency(self, metrics: Dict[str, Any]) -> float:
        """Score efficiency (0-100)"""
        inventory_turnover = metrics.get("inventory_turnover", 0)
        receivables_turnover = metrics.get("receivables_turnover", 0)
        asset_turnover = metrics.get("asset_turnover", 0)
        
        # Inventory turnover scoring (ideal: 5-10)
        if inventory_turnover >= 10:
            it_score = 100
        elif inventory_turnover >= 5:
            it_score = 60 + (inventory_turnover - 5) * 8
        elif inventory_turnover >= 2:
            it_score = 20 + (inventory_turnover - 2) * 13.3
        elif inventory_turnover > 0:
            it_score = inventory_turnover * 10
        else:
            it_score = 50  # No inventory might be OK (services)
        
        # Receivables turnover scoring (ideal: > 10)
        if receivables_turnover >= 12:
            rt_score = 100
        elif receivables_turnover >= 8:
            rt_score = 70 + (receivables_turnover - 8) * 7.5
        elif receivables_turnover >= 4:
            rt_score = 30 + (receivables_turnover - 4) * 10
        elif receivables_turnover > 0:
            rt_score = receivables_turnover * 7.5
        else:
            rt_score = 50
        
        # Asset turnover scoring (ideal: 1.5-2.5)
        if asset_turnover >= 2.0:
            at_score = 100
        elif asset_turnover >= 1.0:
            at_score = 50 + (asset_turnover - 1.0) * 50
        elif asset_turnover >= 0.5:
            at_score = 20 + (asset_turnover - 0.5) * 60
        elif asset_turnover > 0:
            at_score = asset_turnover * 40
        else:
            at_score = 0
        
        return (it_score * 0.35 + rt_score * 0.35 + at_score * 0.30)
    
    def _score_cash_flow(self, metrics: Dict[str, Any]) -> float:
        """Score cash flow health (0-100)"""
        cash_runway = metrics.get("cash_runway_days", 0)
        working_capital = metrics.get("working_capital", 0)
        wc_cycle = metrics.get("working_capital_cycle", 0)
        
        # Cash runway scoring (ideal: > 180 days)
        if cash_runway >= 365:
            cr_score = 100
        elif cash_runway >= 180:
            cr_score = 70 + (cash_runway - 180) * 0.16
        elif cash_runway >= 90:
            cr_score = 40 + (cash_runway - 90) * 0.33
        elif cash_runway >= 30:
            cr_score = 10 + (cash_runway - 30) * 0.5
        else:
            cr_score = cash_runway * 0.33
        
        # Working capital scoring (positive is good)
        if working_capital > 0:
            wc_score = min(100, 50 + (working_capital / 10000) * 5)
        else:
            wc_score = max(0, 50 + (working_capital / 10000) * 5)
        
        # Working capital cycle (lower is better, ideal: 30-60 days)
        if wc_cycle <= 30:
            wcc_score = 100
        elif wc_cycle <= 60:
            wcc_score = 70 + (60 - wc_cycle) * 1
        elif wc_cycle <= 90:
            wcc_score = 40 + (90 - wc_cycle) * 1
        elif wc_cycle <= 120:
            wcc_score = 20 + (120 - wc_cycle) * 0.67
        else:
            wcc_score = max(0, 20 - (wc_cycle - 120) * 0.2)
        
        return (cr_score * 0.4 + wc_score * 0.3 + wcc_score * 0.3)
    
    def _calculate_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        elif score >= 40:
            return "D"
        else:
            return "F"
    
    def _calculate_risk_level(self, score: float) -> str:
        """Determine risk level from score"""
        if score >= 75:
            return "Low"
        elif score >= 55:
            return "Medium"
        elif score >= 35:
            return "High"
        else:
            return "Critical"
