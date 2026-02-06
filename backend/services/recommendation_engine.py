# Recommendation Engine - Financial Product Suggestions
from typing import Dict, Any, List

class RecommendationEngine:
    """Recommend financial products based on company profile and health score"""
    
    # Financial product database (sample)
    FINANCIAL_PRODUCTS = {
        "working_capital_loan": {
            "name": "Working Capital Loan",
            "type": "Loan",
            "providers": ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank"],
            "interest_rate": "10-14%",
            "tenure": "12-36 months",
            "requirements": {
                "min_health_score": 50,
                "min_revenue": 1000000,
                "max_debt_ratio": 0.6
            },
            "best_for": ["Cash flow gaps", "Seasonal businesses", "Inventory purchase"]
        },
        "term_loan": {
            "name": "Business Term Loan",
            "type": "Loan",
            "providers": ["HDFC Bank", "Bajaj Finserv", "Tata Capital"],
            "interest_rate": "11-16%",
            "tenure": "24-60 months",
            "requirements": {
                "min_health_score": 60,
                "min_revenue": 2500000,
                "max_debt_ratio": 0.5
            },
            "best_for": ["Expansion", "Equipment purchase", "Long-term investment"]
        },
        "overdraft": {
            "name": "Overdraft Facility",
            "type": "Credit Line",
            "providers": ["SBI", "HDFC Bank", "Kotak Mahindra"],
            "interest_rate": "12-15%",
            "tenure": "Revolving",
            "requirements": {
                "min_health_score": 55,
                "min_revenue": 500000,
                "max_debt_ratio": 0.7
            },
            "best_for": ["Short-term needs", "Flexible borrowing", "Cash flow management"]
        },
        "invoice_factoring": {
            "name": "Invoice Factoring",
            "type": "Receivables Financing",
            "providers": ["RXIL", "Credlix", "Vayana"],
            "interest_rate": "8-12%",
            "tenure": "30-90 days",
            "requirements": {
                "min_health_score": 40,
                "min_revenue": 1000000
            },
            "best_for": ["Accounts receivable", "B2B businesses", "Quick cash"]
        },
        "equipment_loan": {
            "name": "Equipment Finance",
            "type": "Asset Loan",
            "providers": ["L&T Finance", "Cholamandalam", "Mahindra Finance"],
            "interest_rate": "9-13%",
            "tenure": "24-60 months",
            "requirements": {
                "min_health_score": 55,
                "min_revenue": 1500000,
                "max_debt_ratio": 0.55
            },
            "best_for": ["Manufacturing", "Machinery purchase", "Asset acquisition"]
        },
        "mudra_loan": {
            "name": "MUDRA Loan",
            "type": "Government Scheme",
            "providers": ["All Banks (Govt Scheme)"],
            "interest_rate": "8-12%",
            "tenure": "12-60 months",
            "requirements": {
                "min_health_score": 35,
                "max_loan_amount": 1000000
            },
            "best_for": ["Micro enterprises", "New businesses", "Small funding needs"]
        },
        "trade_credit": {
            "name": "Trade Credit Insurance",
            "type": "Insurance",
            "providers": ["ECGC", "ICICI Lombard", "Tata AIG"],
            "interest_rate": "1-2% premium",
            "tenure": "Annual",
            "requirements": {
                "min_health_score": 45,
                "has_receivables": True
            },
            "best_for": ["Export businesses", "Credit sales", "Risk protection"]
        }
    }
    
    def get_recommendations(
        self,
        health_score: float,
        metrics: Dict[str, Any],
        industry: str,
        company_size: str = "small"
    ) -> List[Dict[str, Any]]:
        """Get recommended financial products"""
        
        recommendations = []
        revenue = metrics.get("raw_values", {}).get("revenue", 0)
        debt_ratio = metrics.get("debt_ratio", 0)
        cash_runway = metrics.get("cash_runway_days", 365)
        working_capital = metrics.get("working_capital", 0)
        
        for product_id, product in self.FINANCIAL_PRODUCTS.items():
            reqs = product.get("requirements", {})
            
            # Check eligibility
            eligible = True
            match_score = 0
            reasons = []
            
            if health_score < reqs.get("min_health_score", 0):
                eligible = False
                reasons.append(f"Health score below {reqs.get('min_health_score')}")
            else:
                match_score += 25
            
            if revenue < reqs.get("min_revenue", 0):
                eligible = False
                reasons.append(f"Revenue below ₹{reqs.get('min_revenue'):,}")
            else:
                match_score += 25
            
            if "max_debt_ratio" in reqs and debt_ratio > reqs["max_debt_ratio"]:
                eligible = False
                reasons.append("Debt ratio too high")
            else:
                match_score += 25
            
            # Context-based scoring
            if cash_runway < 90 and "Cash flow" in str(product.get("best_for", [])):
                match_score += 25
            
            if working_capital < 0 and "working_capital" in product_id:
                match_score += 25
            
            if industry == "Manufacturing" and "equipment" in product_id:
                match_score += 20
            
            if eligible:
                recommendations.append({
                    "product_id": product_id,
                    "name": product["name"],
                    "type": product["type"],
                    "providers": product["providers"][:3],
                    "interest_rate": product["interest_rate"],
                    "tenure": product["tenure"],
                    "match_score": min(100, match_score),
                    "best_for": product["best_for"],
                    "eligibility": "Eligible"
                })
            else:
                # Include as "may qualify" if close
                if health_score >= reqs.get("min_health_score", 0) - 10:
                    recommendations.append({
                        "product_id": product_id,
                        "name": product["name"],
                        "type": product["type"],
                        "providers": product["providers"][:3],
                        "interest_rate": product["interest_rate"],
                        "tenure": product["tenure"],
                        "match_score": max(0, match_score - 30),
                        "best_for": product["best_for"],
                        "eligibility": "May Qualify",
                        "requirements_gap": reasons
                    })
        
        # Sort by match score and return top recommendations
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations[:5]
    
    def get_product_details(self, product_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific product"""
        return self.FINANCIAL_PRODUCTS.get(product_id, {})
