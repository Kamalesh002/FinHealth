"""
Business Insights Service - CFO-style insights and action plan generation
Transforms technical metrics into business-friendly recommendations
"""
from typing import Dict, Any, List, Optional
import os
from services.llm_service import LLMService

class BusinessInsightsService:
    """Generates CFO-style business insights and action plans"""
    
    def __init__(self):
        self.llm = LLMService()
    
    def get_risk_alerts(self, health_score: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate smart risk alerts from health score data"""
        alerts = []
        
        # Extract metrics safely
        metrics = health_score.get('metrics', {})
        overall_score = health_score.get('overall_score', 50)
        risk_factors = health_score.get('risk_factors', [])
        
        # Cash Runway Alert
        cash_runway = metrics.get('cash_runway_days', 180)
        if cash_runway < 90:
            alerts.append({
                'type': 'critical',
                'icon': '🚨',
                'title': 'Cash Runway Critical',
                'message': f'Your business can only sustain operations for {cash_runway} days at current burn rate.',
                'action': 'Reduce expenses or arrange emergency funding immediately.',
                'priority': 1
            })
        elif cash_runway < 180:
            alerts.append({
                'type': 'warning',
                'icon': '⚠️',
                'title': 'Cash Runway Low',
                'message': f'Cash runway of {cash_runway} days requires attention.',
                'action': 'Review cash flow and consider working capital financing.',
                'priority': 2
            })
        
        # Debt Ratio Alert
        debt_to_equity = metrics.get('debt_to_equity', 0)
        if debt_to_equity > 2.0:
            alerts.append({
                'type': 'critical',
                'icon': '🚨',
                'title': 'High Debt Burden',
                'message': f'Debt-to-equity ratio of {debt_to_equity:.1f}x poses significant risk.',
                'action': 'Prioritize debt reduction before seeking new financing.',
                'priority': 1
            })
        elif debt_to_equity > 1.0:
            alerts.append({
                'type': 'warning',
                'icon': '⚠️',
                'title': 'Elevated Debt Levels',
                'message': f'Debt-to-equity of {debt_to_equity:.1f}x is above healthy range.',
                'action': 'Create a debt repayment plan within 6 months.',
                'priority': 3
            })
        
        # Profitability Alert
        net_margin = metrics.get('net_margin', 0)
        if net_margin < 0:
            alerts.append({
                'type': 'critical',
                'icon': '📉',
                'title': 'Operating at Loss',
                'message': f'Net margin of {net_margin:.1f}% means you\'re losing money on every sale.',
                'action': 'Review pricing strategy and cut non-essential costs.',
                'priority': 1
            })
        elif net_margin < 5:
            alerts.append({
                'type': 'warning',
                'icon': '⚠️',
                'title': 'Thin Profit Margins',
                'message': f'Net margin of {net_margin:.1f}% leaves little room for error.',
                'action': 'Identify opportunities to increase prices or reduce costs.',
                'priority': 3
            })
        
        # Liquidity Alert
        current_ratio = metrics.get('current_ratio', 1)
        if current_ratio < 1.0:
            alerts.append({
                'type': 'critical',
                'icon': '💧',
                'title': 'Liquidity Crisis',
                'message': f'Current ratio of {current_ratio:.2f} means you cannot cover short-term obligations.',
                'action': 'Accelerate receivables collection and negotiate supplier terms.',
                'priority': 1
            })
        elif current_ratio < 1.5:
            alerts.append({
                'type': 'warning',
                'icon': '⚠️',
                'title': 'Tight Liquidity',
                'message': f'Current ratio of {current_ratio:.2f} provides limited buffer.',
                'action': 'Build cash reserves to 3 months of operating expenses.',
                'priority': 3
            })
        
        # Working Capital Cycle Alert
        wc_cycle = metrics.get('working_capital_cycle', 0)
        if wc_cycle > 90:
            alerts.append({
                'type': 'warning',
                'icon': '🔄',
                'title': 'Long Cash Conversion Cycle',
                'message': f'Working capital cycle of {wc_cycle} days ties up too much cash.',
                'action': 'Reduce inventory days or negotiate faster customer payments.',
                'priority': 3
            })
        
        # Add positive alerts for good metrics
        if overall_score >= 75:
            alerts.append({
                'type': 'success',
                'icon': '✅',
                'title': 'Strong Financial Health',
                'message': f'Health score of {overall_score:.0f} indicates robust financial position.',
                'action': 'Consider growth investments or expansion opportunities.',
                'priority': 5
            })
        
        if net_margin > 15:
            alerts.append({
                'type': 'success',
                'icon': '📈',
                'title': 'Excellent Profitability',
                'message': f'Net margin of {net_margin:.1f}% is well above industry average.',
                'action': 'Reinvest profits in high-growth areas.',
                'priority': 5
            })
        
        # Sort by priority (1 = most critical)
        alerts.sort(key=lambda x: x['priority'])
        
        return alerts[:6]  # Return top 6 alerts
    
    def get_cfo_insights(self, health_score: Dict[str, Any], industry: str) -> List[Dict[str, Any]]:
        """Transform metrics into CFO-style business insights"""
        insights = []
        metrics = health_score.get('metrics', {})
        overall_score = health_score.get('overall_score', 50)
        
        # Generate business-language insights
        insights.append({
            'category': 'Overall Health',
            'metric_name': 'Financial Health Score',
            'metric_value': f'{overall_score:.0f}/100',
            'interpretation': self._interpret_health_score(overall_score),
            'color': self._get_score_color(overall_score)
        })
        
        # Cash Position
        cash_runway = metrics.get('cash_runway_days', 180)
        insights.append({
            'category': 'Cash Position',
            'metric_name': 'Cash Runway',
            'metric_value': f'{cash_runway} days',
            'interpretation': self._interpret_cash_runway(cash_runway),
            'color': 'success' if cash_runway > 180 else 'warning' if cash_runway > 90 else 'danger'
        })
        
        # Debt Health
        debt_to_equity = metrics.get('debt_to_equity', 0)
        insights.append({
            'category': 'Debt Health',
            'metric_name': 'Debt Level',
            'metric_value': f'{debt_to_equity:.1f}x',
            'interpretation': self._interpret_debt(debt_to_equity),
            'color': 'success' if debt_to_equity < 0.5 else 'warning' if debt_to_equity < 1.5 else 'danger'
        })
        
        # Profitability
        net_margin = metrics.get('net_margin', 0)
        insights.append({
            'category': 'Profitability',
            'metric_name': 'Profit per Sale',
            'metric_value': f'{net_margin:.1f}%',
            'interpretation': self._interpret_margin(net_margin),
            'color': 'success' if net_margin > 10 else 'warning' if net_margin > 0 else 'danger'
        })
        
        # Liquidity
        current_ratio = metrics.get('current_ratio', 1)
        insights.append({
            'category': 'Bill Paying Ability',
            'metric_name': 'Short-term Coverage',
            'metric_value': f'{current_ratio:.2f}x',
            'interpretation': self._interpret_liquidity(current_ratio),
            'color': 'success' if current_ratio > 2 else 'warning' if current_ratio > 1 else 'danger'
        })
        
        # Efficiency
        wc_cycle = metrics.get('working_capital_cycle', 0)
        insights.append({
            'category': 'Cash Efficiency',
            'metric_name': 'Cash Conversion',
            'metric_value': f'{wc_cycle} days',
            'interpretation': self._interpret_wc_cycle(wc_cycle),
            'color': 'success' if wc_cycle < 60 else 'warning' if wc_cycle < 90 else 'danger'
        })
        
        return insights
    
    async def generate_action_plan(self, health_score: Dict[str, Any], company_name: str, industry: str) -> Dict[str, Any]:
        """Generate a 90-day action plan using AI"""
        metrics = health_score.get('metrics', {})
        risk_factors = health_score.get('risk_factors', [])
        overall_score = health_score.get('overall_score', 50)
        
        # Build context for AI
        context = f"""
Company: {company_name}
Industry: {industry}
Health Score: {overall_score}/100
Key Metrics:
- Cash Runway: {metrics.get('cash_runway_days', 'N/A')} days
- Net Margin: {metrics.get('net_margin', 'N/A')}%
- Current Ratio: {metrics.get('current_ratio', 'N/A')}
- Debt-to-Equity: {metrics.get('debt_to_equity', 'N/A')}
- Working Capital Cycle: {metrics.get('working_capital_cycle', 'N/A')} days

Risk Factors:
{chr(10).join(['- ' + str(rf) for rf in risk_factors[:5]])}
"""
        
        prompt = f"""As a Chief Financial Officer advisor for SMEs, create a practical 90-day financial improvement action plan.

{context}

Generate a structured action plan with:
1. TOP PRIORITY (Days 1-30): 2-3 immediate actions to address critical issues
2. MEDIUM PRIORITY (Days 31-60): 2-3 structural improvements
3. LONG-TERM (Days 61-90): 2-3 growth-focused actions

For each action, include:
- Specific action (one sentence)
- Expected benefit (quantified if possible)
- Who should execute it

Format as a structured plan. Be specific and practical for a small business. No generic advice."""

        try:
            response = await self.llm.generate_response(prompt)
            
            # Parse into structured format
            action_plan = {
                'company_name': company_name,
                'generated_date': 'Today',
                'health_score': overall_score,
                'plan_content': response,
                'summary': self._get_plan_summary(overall_score),
                'phases': [
                    {
                        'name': 'Immediate Actions',
                        'days': '1-30',
                        'focus': 'Address critical issues',
                        'icon': '🚀'
                    },
                    {
                        'name': 'Structural Improvements',
                        'days': '31-60',
                        'focus': 'Build stronger foundation',
                        'icon': '🏗️'
                    },
                    {
                        'name': 'Growth Actions',
                        'days': '61-90',
                        'focus': 'Position for growth',
                        'icon': '📈'
                    }
                ]
            }
            return action_plan
            
        except Exception as e:
            # Fallback to template-based plan
            return self._generate_fallback_plan(health_score, company_name, industry)
    
    def _interpret_health_score(self, score: float) -> str:
        if score >= 80:
            return "Your business is financially healthy and well-positioned for growth."
        elif score >= 60:
            return "Your business is stable but has room for improvement in key areas."
        elif score >= 40:
            return "Your business faces some financial challenges that need attention."
        else:
            return "Your business needs urgent financial intervention to survive."
    
    def _interpret_cash_runway(self, days: int) -> str:
        if days > 180:
            return "You have comfortable cash reserves to weather unexpected challenges."
        elif days > 90:
            return "Cash position is adequate but consider building more reserves."
        elif days > 30:
            return "Cash is tight. Focus on improving collections and reducing expenses."
        else:
            return "Immediate cash crisis. Prioritize emergency funding or cost cuts."
    
    def _interpret_debt(self, ratio: float) -> str:
        if ratio < 0.3:
            return "Very low debt gives you financial flexibility and borrowing capacity."
        elif ratio < 1.0:
            return "Debt is manageable and within healthy range for most businesses."
        elif ratio < 2.0:
            return "Debt is elevated. New loans may be expensive or hard to obtain."
        else:
            return "High debt burden limits options and increases financial risk."
    
    def _interpret_margin(self, margin: float) -> str:
        if margin > 15:
            return "Excellent profitability. You're earning well above cost."
        elif margin > 5:
            return "Reasonable profit margins for most industries."
        elif margin > 0:
            return "Thin margins leave little room for error."
        else:
            return "Operating at a loss. Each sale costs more than it earns."
    
    def _interpret_liquidity(self, ratio: float) -> str:
        if ratio > 2.0:
            return "Strong ability to pay bills. No short-term cash concerns."
        elif ratio > 1.5:
            return "Good short-term financial position."
        elif ratio > 1.0:
            return "Can cover bills but margin is thin. Build more buffer."
        else:
            return "Cannot cover short-term obligations from current assets."
    
    def _interpret_wc_cycle(self, days: int) -> str:
        if days < 30:
            return "Excellent cash efficiency. Money cycles back quickly."
        elif days < 60:
            return "Good working capital management."
        elif days < 90:
            return "Cash takes time to cycle back. Look to speed this up."
        else:
            return "Too much cash tied up in operations. Review inventory and receivables."
    
    def _get_score_color(self, score: float) -> str:
        if score >= 80:
            return 'success'
        elif score >= 60:
            return 'info'
        elif score >= 40:
            return 'warning'
        return 'danger'
    
    def _get_plan_summary(self, score: float) -> str:
        if score >= 80:
            return "Focus on growth optimization and market expansion opportunities."
        elif score >= 60:
            return "Strengthen financial foundation while addressing minor weaknesses."
        elif score >= 40:
            return "Prioritize cash flow improvement and cost optimization."
        else:
            return "Emergency stabilization plan with focus on survival and recovery."
    
    def _generate_fallback_plan(self, health_score: Dict, company_name: str, industry: str) -> Dict:
        """Generate a template-based plan when AI is unavailable"""
        overall_score = health_score.get('overall_score', 50)
        metrics = health_score.get('metrics', {})
        
        plan_content = f"""# 90-Day Financial Recovery Plan for {company_name}

## Phase 1: Immediate Actions (Days 1-30)
🎯 **Focus: Stabilize Cash Position**

1. **Review All Receivables**
   - Action: Contact all customers with overdue payments
   - Expected Impact: Recover 20-30% of outstanding receivables
   - Owner: Finance/Accounts team

2. **Expense Audit**
   - Action: Identify and eliminate non-essential expenses
   - Expected Impact: Reduce monthly burn by 10-15%
   - Owner: CFO/Business Owner

3. **Inventory Optimization**
   - Action: Identify slow-moving inventory for liquidation
   - Expected Impact: Free up cash tied in dead stock
   - Owner: Operations team

## Phase 2: Structural Improvements (Days 31-60)
🏗️ **Focus: Build Stronger Foundation**

1. **Negotiate Supplier Terms**
   - Action: Request extended payment terms from top 5 suppliers
   - Expected Impact: Improve cash flow by 15-20 days
   - Owner: Procurement team

2. **Implement Cash Flow Forecasting**
   - Action: Create 13-week rolling cash forecast
   - Expected Impact: Better visibility and planning
   - Owner: Finance team

3. **Review Pricing Strategy**
   - Action: Analyze margins by product/service line
   - Expected Impact: Identify opportunities for price optimization
   - Owner: Sales and Finance teams

## Phase 3: Growth Actions (Days 61-90)
📈 **Focus: Position for Sustainable Growth**

1. **Explore Financing Options**
   - Action: Research suitable financing products
   - Expected Impact: Secure growth capital at favorable terms
   - Owner: Business Owner

2. **Customer Segmentation**
   - Action: Identify most profitable customer segments
   - Expected Impact: Focus resources on high-value customers
   - Owner: Sales team

3. **Process Automation**
   - Action: Identify manual processes for automation
   - Expected Impact: Reduce operational costs by 10%
   - Owner: Operations team
"""
        
        return {
            'company_name': company_name,
            'generated_date': 'Today',
            'health_score': overall_score,
            'plan_content': plan_content,
            'summary': self._get_plan_summary(overall_score),
            'phases': [
                {'name': 'Immediate Actions', 'days': '1-30', 'focus': 'Stabilize Cash', 'icon': '🎯'},
                {'name': 'Structural Improvements', 'days': '31-60', 'focus': 'Build Foundation', 'icon': '🏗️'},
                {'name': 'Growth Actions', 'days': '61-90', 'focus': 'Position for Growth', 'icon': '📈'}
            ]
        }
