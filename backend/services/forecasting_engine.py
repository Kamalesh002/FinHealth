# Forecasting Engine - Financial Projections
from typing import Dict, Any, List
from datetime import datetime, timedelta

class ForecastingEngine:
    """Generate financial forecasts and projections"""
    
    # Industry growth rates (average annual %)
    INDUSTRY_GROWTH_RATES = {
        "Manufacturing": {"base": 8, "optimistic": 15, "pessimistic": 3},
        "Retail": {"base": 10, "optimistic": 18, "pessimistic": 4},
        "Agriculture": {"base": 5, "optimistic": 12, "pessimistic": -2},
        "Services": {"base": 12, "optimistic": 22, "pessimistic": 5},
        "Logistics": {"base": 10, "optimistic": 18, "pessimistic": 4},
        "E-commerce": {"base": 20, "optimistic": 35, "pessimistic": 8}
    }
    
    def generate_forecast(
        self, 
        raw_data: Dict[str, Any], 
        industry: str
    ) -> Dict[str, Any]:
        """Generate financial forecasts based on historical data"""
        
        # Extract current financial values
        financials = self._extract_current_values(raw_data)
        growth_rates = self.INDUSTRY_GROWTH_RATES.get(
            industry, 
            {"base": 10, "optimistic": 18, "pessimistic": 5}
        )
        
        # Generate projections
        projections = {
            "revenue_forecast": self._forecast_revenue(financials, growth_rates),
            "cash_flow_projection": self._forecast_cash_flow(financials),
            "break_even_analysis": self._calculate_break_even(financials),
            "growth_scenarios": self._generate_scenarios(financials, growth_rates),
            "cash_runway_projection": self._project_cash_runway(financials),
            "key_metrics_trend": self._project_key_metrics(financials, growth_rates)
        }
        
        return projections
    
    def _extract_current_values(self, raw_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract current financial values from raw data"""
        financials = {
            "revenue": 0,
            "expenses": 0,
            "profit": 0,
            "cash": 0,
            "monthly_burn": 0
        }
        
        if "summary" in raw_data:
            summary = raw_data["summary"]
            financials["revenue"] = summary.get("total_revenue", 0)
            financials["expenses"] = summary.get("total_expenses", 0)
            financials["profit"] = summary.get("total_profit", 0)
        
        if "financial_data" in raw_data:
            for col, info in raw_data["financial_data"].items():
                category = info.get("category", "")
                total = info.get("total", 0)
                
                if category == "revenue":
                    financials["revenue"] += total
                elif category == "expense":
                    financials["expenses"] += total
                elif "cash" in col.lower():
                    financials["cash"] += total
        
        # Calculate monthly burn rate
        financials["monthly_burn"] = financials["expenses"] / 12 if financials["expenses"] > 0 else 0
        financials["profit"] = financials["revenue"] - financials["expenses"]
        
        return financials
    
    def _forecast_revenue(
        self, 
        financials: Dict[str, float], 
        growth_rates: Dict[str, float]
    ) -> Dict[str, Any]:
        """Forecast revenue for next 12 months"""
        current_revenue = financials.get("revenue", 0)
        monthly_revenue = current_revenue / 12
        
        forecasts = {
            "3_month": {},
            "6_month": {},
            "12_month": {}
        }
        
        for scenario, annual_rate in growth_rates.items():
            monthly_rate = annual_rate / 12 / 100
            
            forecasts["3_month"][scenario] = round(
                monthly_revenue * 3 * (1 + monthly_rate * 3), 2
            )
            forecasts["6_month"][scenario] = round(
                monthly_revenue * 6 * (1 + monthly_rate * 6), 2
            )
            forecasts["12_month"][scenario] = round(
                current_revenue * (1 + annual_rate / 100), 2
            )
        
        # Monthly breakdown for base scenario
        monthly_forecast = []
        base_monthly_rate = growth_rates["base"] / 12 / 100
        
        for month in range(1, 13):
            projected = monthly_revenue * (1 + base_monthly_rate * month)
            monthly_forecast.append({
                "month": month,
                "projected_revenue": round(projected, 2)
            })
        
        return {
            "current_annual_revenue": current_revenue,
            "forecasts": forecasts,
            "monthly_breakdown": monthly_forecast
        }
    
    def _forecast_cash_flow(self, financials: Dict[str, float]) -> Dict[str, Any]:
        """Project cash flow for next 6 months"""
        cash = financials.get("cash", 0)
        monthly_revenue = financials.get("revenue", 0) / 12
        monthly_expenses = financials.get("monthly_burn", 0)
        
        monthly_projection = []
        running_cash = cash
        
        for month in range(1, 7):
            inflow = monthly_revenue * (1 + 0.01 * month)  # Slight growth
            outflow = monthly_expenses * (1 + 0.005 * month)  # Slight increase
            net_flow = inflow - outflow
            running_cash += net_flow
            
            monthly_projection.append({
                "month": month,
                "inflow": round(inflow, 2),
                "outflow": round(outflow, 2),
                "net_flow": round(net_flow, 2),
                "ending_cash": round(running_cash, 2)
            })
        
        return {
            "starting_cash": cash,
            "monthly_projection": monthly_projection,
            "projected_cash_6m": round(running_cash, 2),
            "average_monthly_net_flow": round(
                sum(p["net_flow"] for p in monthly_projection) / 6, 2
            )
        }
    
    def _calculate_break_even(self, financials: Dict[str, float]) -> Dict[str, Any]:
        """Calculate break-even analysis"""
        revenue = financials.get("revenue", 0)
        expenses = financials.get("expenses", 0)
        profit = financials.get("profit", 0)
        
        # Assume 30% of costs are fixed, 70% variable
        fixed_costs = expenses * 0.3
        variable_costs = expenses * 0.7
        variable_cost_ratio = variable_costs / revenue if revenue > 0 else 0.7
        
        # Break-even revenue
        contribution_margin = 1 - variable_cost_ratio
        break_even_revenue = fixed_costs / contribution_margin if contribution_margin > 0 else 0
        
        # Current position
        if revenue > 0:
            break_even_percentage = (break_even_revenue / revenue) * 100
            margin_of_safety = ((revenue - break_even_revenue) / revenue) * 100
        else:
            break_even_percentage = 0
            margin_of_safety = 0
        
        return {
            "break_even_revenue": round(break_even_revenue, 2),
            "current_revenue": revenue,
            "break_even_percentage": round(break_even_percentage, 1),
            "margin_of_safety": round(margin_of_safety, 1),
            "is_profitable": profit > 0,
            "fixed_costs_estimate": round(fixed_costs, 2),
            "contribution_margin": round(contribution_margin * 100, 1)
        }
    
    def _generate_scenarios(
        self, 
        financials: Dict[str, float],
        growth_rates: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Generate optimistic, base, and pessimistic scenarios"""
        revenue = financials.get("revenue", 0)
        profit = financials.get("profit", 0)
        
        scenarios = []
        
        for scenario_name, growth_rate in growth_rates.items():
            projected_revenue = revenue * (1 + growth_rate / 100)
            # Assume profit margin stays relatively constant
            profit_margin = profit / revenue if revenue > 0 else 0.1
            projected_profit = projected_revenue * profit_margin
            
            scenarios.append({
                "scenario": scenario_name,
                "growth_rate": growth_rate,
                "projected_revenue": round(projected_revenue, 2),
                "projected_profit": round(projected_profit, 2),
                "description": self._get_scenario_description(scenario_name)
            })
        
        return scenarios
    
    def _get_scenario_description(self, scenario: str) -> str:
        """Get description for scenario"""
        descriptions = {
            "optimistic": "Best case with strong market growth and operational efficiency",
            "base": "Expected outcome based on current trends and industry averages",
            "pessimistic": "Conservative estimate accounting for potential challenges"
        }
        return descriptions.get(scenario, "Projected scenario")
    
    def _project_cash_runway(self, financials: Dict[str, float]) -> Dict[str, Any]:
        """Project cash runway under different scenarios"""
        cash = financials.get("cash", 0)
        monthly_burn = financials.get("monthly_burn", 0)
        
        if monthly_burn <= 0:
            return {
                "current_runway_months": 24,
                "status": "positive_cash_flow",
                "message": "Company is generating positive cash flow"
            }
        
        current_runway = cash / monthly_burn
        
        # Project with different expense scenarios
        scenarios = {
            "current": current_runway,
            "10_percent_reduction": cash / (monthly_burn * 0.9),
            "20_percent_reduction": cash / (monthly_burn * 0.8),
            "10_percent_increase": cash / (monthly_burn * 1.1)
        }
        
        return {
            "current_cash": cash,
            "monthly_burn_rate": round(monthly_burn, 2),
            "current_runway_months": round(current_runway, 1),
            "scenarios": {k: round(v, 1) for k, v in scenarios.items()},
            "critical_date": (
                datetime.now() + timedelta(days=current_runway * 30)
            ).strftime("%Y-%m-%d") if current_runway < 12 else None
        }
    
    def _project_key_metrics(
        self, 
        financials: Dict[str, float],
        growth_rates: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Project key metrics trend"""
        base_rate = growth_rates.get("base", 10) / 100
        
        return [
            {
                "metric": "Revenue",
                "current": financials.get("revenue", 0),
                "3m_projection": round(financials.get("revenue", 0) * (1 + base_rate * 0.25), 2),
                "6m_projection": round(financials.get("revenue", 0) * (1 + base_rate * 0.5), 2),
                "12m_projection": round(financials.get("revenue", 0) * (1 + base_rate), 2)
            },
            {
                "metric": "Profit",
                "current": financials.get("profit", 0),
                "3m_projection": round(financials.get("profit", 0) * (1 + base_rate * 0.3), 2),
                "6m_projection": round(financials.get("profit", 0) * (1 + base_rate * 0.6), 2),
                "12m_projection": round(financials.get("profit", 0) * (1 + base_rate * 1.1), 2)
            }
        ]
