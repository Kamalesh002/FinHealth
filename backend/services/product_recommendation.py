"""
Financial Product Recommendation Engine
Recommends suitable financial products based on company health and needs
"""
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ProductType(Enum):
    WORKING_CAPITAL_LOAN = "working_capital_loan"
    TERM_LOAN = "term_loan"
    INVOICE_DISCOUNTING = "invoice_discounting"
    MSME_CREDIT_LINE = "msme_credit_line"
    EQUIPMENT_FINANCING = "equipment_financing"
    TRADE_FINANCE = "trade_finance"
    OVERDRAFT_FACILITY = "overdraft_facility"
    GOVERNMENT_SCHEME = "government_scheme"


@dataclass
class FinancialProduct:
    """Financial product definition"""
    id: str
    name: str
    type: ProductType
    description: str
    provider_type: str  # Bank, NBFC, Government
    min_score: int  # Minimum health score required
    max_score: int  # Maximum health score (for risk-based products)
    interest_rate_range: str
    tenure_range: str
    loan_amount_range: str
    eligibility_criteria: List[str]
    ideal_for: List[str]
    features: List[str]
    documents_required: List[str]


# Product Database
FINANCIAL_PRODUCTS: List[FinancialProduct] = [
    FinancialProduct(
        id="wcl_001",
        name="Working Capital Loan",
        type=ProductType.WORKING_CAPITAL_LOAN,
        description="Short-term financing to manage daily operations, payroll, and inventory needs",
        provider_type="Bank/NBFC",
        min_score=45,
        max_score=100,
        interest_rate_range="10% - 18% p.a.",
        tenure_range="6 months - 3 years",
        loan_amount_range="₹5 Lakh - ₹5 Crore",
        eligibility_criteria=[
            "Business operational for 2+ years",
            "Annual turnover > ₹25 Lakhs",
            "Good repayment history"
        ],
        ideal_for=["Cash flow gaps", "Seasonal inventory", "Bulk purchases"],
        features=["Quick disbursement", "Flexible repayment", "No collateral up to ₹50L"],
        documents_required=["GST returns", "Bank statements", "Financial statements"]
    ),
    FinancialProduct(
        id="inv_001",
        name="Invoice Discounting",
        type=ProductType.INVOICE_DISCOUNTING,
        description="Get immediate cash against unpaid invoices from creditworthy customers",
        provider_type="NBFC/Fintech",
        min_score=40,
        max_score=100,
        interest_rate_range="12% - 24% p.a.",
        tenure_range="30 - 90 days",
        loan_amount_range="Up to 90% of invoice value",
        eligibility_criteria=[
            "B2B business model",
            "Invoices from reputed companies",
            "Invoice value > ₹1 Lakh"
        ],
        ideal_for=["High receivables", "Long payment cycles", "Cash flow crunch"],
        features=["No fixed EMI", "Pay only for days used", "Quick approval"],
        documents_required=["Invoices", "Purchase orders", "Customer details"]
    ),
    FinancialProduct(
        id="msme_001",
        name="MSME Credit Line",
        type=ProductType.MSME_CREDIT_LINE,
        description="Revolving credit facility for registered MSMEs with flexible drawdown",
        provider_type="Bank",
        min_score=50,
        max_score=100,
        interest_rate_range="9% - 14% p.a.",
        tenure_range="1 - 5 years",
        loan_amount_range="₹10 Lakh - ₹2 Crore",
        eligibility_criteria=[
            "MSME/Udyam registration",
            "3+ years in business",
            "Positive cash flow"
        ],
        ideal_for=["Regular working capital needs", "Expansion", "Equipment purchase"],
        features=["Draw as needed", "Interest only on usage", "Government subsidy available"],
        documents_required=["Udyam certificate", "ITR", "Bank statements", "GST returns"]
    ),
    FinancialProduct(
        id="od_001",
        name="Overdraft Facility",
        type=ProductType.OVERDRAFT_FACILITY,
        description="Withdraw more than your account balance up to a sanctioned limit",
        provider_type="Bank",
        min_score=55,
        max_score=100,
        interest_rate_range="10% - 16% p.a.",
        tenure_range="Renewable annually",
        loan_amount_range="₹5 Lakh - ₹1 Crore",
        eligibility_criteria=[
            "Existing bank relationship",
            "Good account transaction history",
            "Stable business income"
        ],
        ideal_for=["Short-term cash gaps", "Emergency expenses", "Salary disbursement"],
        features=["Instant access", "Pay interest only on usage", "No prepayment penalty"],
        documents_required=["Bank statements", "Business proof", "KYC documents"]
    ),
    FinancialProduct(
        id="tl_001",
        name="Business Term Loan",
        type=ProductType.TERM_LOAN,
        description="Lump sum financing for major business investments with fixed EMIs",
        provider_type="Bank/NBFC",
        min_score=55,
        max_score=100,
        interest_rate_range="11% - 18% p.a.",
        tenure_range="1 - 7 years",
        loan_amount_range="₹10 Lakh - ₹10 Crore",
        eligibility_criteria=[
            "Profitable for 2+ years",
            "Strong financial statements",
            "Collateral may be required"
        ],
        ideal_for=["Expansion", "New location", "Major equipment", "Acquisition"],
        features=["Fixed EMI", "Long tenure", "Higher amounts"],
        documents_required=["Audited financials", "Project report", "Collateral documents"]
    ),
    FinancialProduct(
        id="ef_001",
        name="Equipment Financing",
        type=ProductType.EQUIPMENT_FINANCING,
        description="Finance for purchasing machinery, vehicles, or equipment",
        provider_type="Bank/NBFC",
        min_score=45,
        max_score=100,
        interest_rate_range="10% - 16% p.a.",
        tenure_range="1 - 5 years",
        loan_amount_range="Up to 100% of equipment cost",
        eligibility_criteria=[
            "1+ years in business",
            "Valid quotation from vendor",
            "Equipment as collateral"
        ],
        ideal_for=["Machinery purchase", "Vehicle fleet", "Technology upgrade"],
        features=["Equipment as security", "Tax benefits", "Quick processing"],
        documents_required=["Proforma invoice", "Business proof", "Bank statements"]
    ),
    FinancialProduct(
        id="mudra_001",
        name="MUDRA Loan (Government Scheme)",
        type=ProductType.GOVERNMENT_SCHEME,
        description="Government-backed loans for micro enterprises under PM Mudra Yojana",
        provider_type="Government/Bank",
        min_score=30,
        max_score=70,
        interest_rate_range="7% - 12% p.a.",
        tenure_range="Up to 5 years",
        loan_amount_range="₹50,000 - ₹10 Lakh",
        eligibility_criteria=[
            "Non-farm income generating activity",
            "Not a defaulter",
            "Micro enterprise category"
        ],
        ideal_for=["Small businesses", "First-time borrowers", "Low-cost financing"],
        features=["No collateral required", "Lower interest rates", "Easy approval"],
        documents_required=["Aadhar", "PAN", "Business plan", "Address proof"]
    ),
    FinancialProduct(
        id="standup_001",
        name="Stand Up India Loan",
        type=ProductType.GOVERNMENT_SCHEME,
        description="Government scheme for SC/ST and women entrepreneurs",
        provider_type="Government/Bank",
        min_score=25,
        max_score=80,
        interest_rate_range="7.25% - 10% p.a.",
        tenure_range="Up to 7 years",
        loan_amount_range="₹10 Lakh - ₹1 Crore",
        eligibility_criteria=[
            "SC/ST or Woman entrepreneur",
            "First-time borrower for business",
            "Manufacturing/Services/Trading"
        ],
        ideal_for=["New ventures", "First business loan", "Greenfield projects"],
        features=["Composite loan", "Moratorium period", "Refinance available"],
        documents_required=["Caste/Gender certificate", "Project report", "KYC"]
    ),
    FinancialProduct(
        id="tf_001",
        name="Trade Finance",
        type=ProductType.TRADE_FINANCE,
        description="Financing for import/export transactions and international trade",
        provider_type="Bank",
        min_score=55,
        max_score=100,
        interest_rate_range="8% - 14% p.a.",
        tenure_range="30 - 180 days",
        loan_amount_range="Based on LC/invoice value",
        eligibility_criteria=[
            "Import/Export license",
            "International trade history",
            "Bank relationship"
        ],
        ideal_for=["Importers", "Exporters", "International suppliers"],
        features=["LC backed", "Currency hedging", "Export incentives"],
        documents_required=["Import/Export docs", "LC", "Custom papers"]
    ),
]


class ProductRecommendationEngine:
    """Recommends financial products based on company profile and financial health"""
    
    def __init__(self):
        self.products = FINANCIAL_PRODUCTS
    
    def get_recommendations(
        self,
        health_score: float,
        metrics: Dict[str, Any],
        industry: str,
        company_age_years: int = 2
    ) -> Dict[str, Any]:
        """
        Get personalized product recommendations based on financial profile
        
        Args:
            health_score: Overall health score (0-100)
            metrics: Financial metrics dictionary
            industry: Industry type
            company_age_years: Years in business
            
        Returns:
            Dictionary with recommended products and reasoning
        """
        
        recommendations = []
        
        for product in self.products:
            score, reasons = self._calculate_fit_score(
                product, health_score, metrics, industry, company_age_years
            )
            
            if score > 0:
                recommendations.append({
                    "product": self._product_to_dict(product),
                    "fit_score": score,
                    "match_reasons": reasons,
                    "qualification_status": self._get_qualification_status(score)
                })
        
        # Sort by fit score
        recommendations.sort(key=lambda x: x["fit_score"], reverse=True)
        
        # Categorize recommendations
        result = {
            "highly_recommended": [r for r in recommendations if r["fit_score"] >= 80][:3],
            "good_options": [r for r in recommendations if 60 <= r["fit_score"] < 80][:3],
            "consider_later": [r for r in recommendations if 40 <= r["fit_score"] < 60][:2],
            "summary": self._generate_summary(recommendations[:3], health_score, metrics),
            "next_steps": self._generate_next_steps(recommendations[:3])
        }
        
        return result
    
    def _calculate_fit_score(
        self,
        product: FinancialProduct,
        health_score: float,
        metrics: Dict[str, Any],
        industry: str,
        company_age_years: int
    ) -> tuple:
        """Calculate how well a product fits the company's needs"""
        
        score = 0
        reasons = []
        
        # Check health score eligibility
        if health_score < product.min_score:
            return 0, ["Health score below minimum requirement"]
        
        if health_score > product.max_score:
            # Some products are meant for lower-scoring companies
            pass
        
        # Base score from health score fit
        score_fit = min(100, (health_score - product.min_score) / (product.max_score - product.min_score) * 100)
        score += score_fit * 0.3
        
        # Check specific needs based on metrics
        cash_runway = metrics.get("cash_runway_days", 180)
        current_ratio = metrics.get("current_ratio", 1.5)
        receivables_days = metrics.get("receivables_days", 30)
        net_margin = metrics.get("net_margin", 5)
        
        # Working capital needs
        if product.type == ProductType.WORKING_CAPITAL_LOAN:
            if cash_runway < 90:
                score += 25
                reasons.append("Low cash runway - working capital needed")
            if current_ratio < 1.2:
                score += 15
                reasons.append("Tight liquidity position")
        
        # Invoice discounting fit
        if product.type == ProductType.INVOICE_DISCOUNTING:
            if receivables_days > 45:
                score += 30
                reasons.append(f"High receivables ({receivables_days} days)")
            if cash_runway < 60 and receivables_days > 30:
                score += 20
                reasons.append("Can convert receivables to immediate cash")
        
        # MSME Credit Line
        if product.type == ProductType.MSME_CREDIT_LINE:
            if company_age_years >= 3:
                score += 20
                reasons.append("Established business qualifies for credit line")
        
        # Government schemes for struggling businesses
        if product.type == ProductType.GOVERNMENT_SCHEME:
            if health_score < 60:
                score += 25
                reasons.append("Government schemes ideal for rebuilding")
            if health_score >= 60:
                score -= 10  # Reduce priority for healthier businesses
        
        # Term loan for healthy, growing businesses
        if product.type == ProductType.TERM_LOAN:
            if health_score >= 65 and net_margin > 5:
                score += 25
                reasons.append("Strong profile for term loan")
        
        # Overdraft for established relationships
        if product.type == ProductType.OVERDRAFT_FACILITY:
            if company_age_years >= 2:
                score += 15
                reasons.append("Overdraft suitable for established business")
        
        # Industry-specific adjustments
        if industry in ["Manufacturing", "Retail"]:
            if product.type == ProductType.EQUIPMENT_FINANCING:
                score += 15
                reasons.append(f"Equipment financing common in {industry}")
        
        if industry in ["E-commerce", "Services"]:
            if product.type == ProductType.INVOICE_DISCOUNTING:
                score += 10
                reasons.append(f"Invoice discounting popular in {industry}")
        
        return min(100, score), reasons
    
    def _product_to_dict(self, product: FinancialProduct) -> Dict[str, Any]:
        """Convert product to dictionary"""
        return {
            "id": product.id,
            "name": product.name,
            "type": product.type.value,
            "description": product.description,
            "provider_type": product.provider_type,
            "interest_rate_range": product.interest_rate_range,
            "tenure_range": product.tenure_range,
            "loan_amount_range": product.loan_amount_range,
            "eligibility_criteria": product.eligibility_criteria,
            "ideal_for": product.ideal_for,
            "features": product.features,
            "documents_required": product.documents_required
        }
    
    def _get_qualification_status(self, fit_score: float) -> str:
        """Get qualification status based on fit score"""
        if fit_score >= 80:
            return "highly_likely"
        elif fit_score >= 60:
            return "likely"
        elif fit_score >= 40:
            return "possible"
        else:
            return "needs_improvement"
    
    def _generate_summary(
        self,
        top_recommendations: List[Dict],
        health_score: float,
        metrics: Dict[str, Any]
    ) -> str:
        """Generate a summary of recommendations"""
        
        if not top_recommendations:
            return "Based on your current financial profile, we recommend focusing on improving your health score before applying for financing."
        
        cash_runway = metrics.get("cash_runway_days", 180)
        
        if health_score >= 70:
            return f"Your strong financial health (score: {health_score:.0f}) opens doors to multiple financing options. We recommend exploring {top_recommendations[0]['product']['name']} as your primary option."
        elif health_score >= 50:
            if cash_runway < 60:
                return f"With a moderate health score ({health_score:.0f}) and tight cash runway ({cash_runway} days), we recommend invoice discounting or working capital loans for immediate relief."
            return f"Your moderate financial health ({health_score:.0f}) qualifies you for several products. Consider MSME schemes for better rates."
        else:
            return f"With a developing health score ({health_score:.0f}), we recommend government-backed schemes like MUDRA loans which have flexible eligibility."
    
    def _generate_next_steps(self, top_recommendations: List[Dict]) -> List[str]:
        """Generate actionable next steps"""
        
        if not top_recommendations:
            return [
                "Focus on improving cash flow",
                "Build 3-6 months of cash reserves",
                "Improve receivables collection"
            ]
        
        steps = [
            f"Gather documents for {top_recommendations[0]['product']['name']}",
            "Update your GST returns and bank statements",
            "Check your CIBIL score",
        ]
        
        if len(top_recommendations) > 1:
            steps.append(f"Compare rates between {top_recommendations[0]['product']['name']} and {top_recommendations[1]['product']['name']}")
        
        return steps[:4]
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Get all available financial products"""
        return [self._product_to_dict(p) for p in self.products]
