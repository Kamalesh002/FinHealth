# Industry Benchmark Service
from typing import Dict, Any

class IndustryBenchmark:
    """Industry-specific benchmarking data and comparison"""
    
    # Industry benchmark data (Indian SME averages)
    BENCHMARKS = {
        "Manufacturing": {
            "current_ratio": {"low": 1.2, "median": 1.5, "high": 2.0},
            "quick_ratio": {"low": 0.8, "median": 1.0, "high": 1.3},
            "gross_margin": {"low": 20, "median": 30, "high": 40},
            "net_margin": {"low": 5, "median": 10, "high": 15},
            "debt_to_equity": {"low": 0.8, "median": 1.2, "high": 1.8},
            "inventory_turnover": {"low": 4, "median": 6, "high": 10},
            "asset_turnover": {"low": 0.8, "median": 1.2, "high": 1.8},
            "cash_runway_days": {"low": 60, "median": 120, "high": 200}
        },
        "Retail": {
            "current_ratio": {"low": 1.0, "median": 1.3, "high": 1.8},
            "quick_ratio": {"low": 0.5, "median": 0.8, "high": 1.2},
            "gross_margin": {"low": 25, "median": 35, "high": 50},
            "net_margin": {"low": 3, "median": 6, "high": 12},
            "debt_to_equity": {"low": 0.5, "median": 1.0, "high": 1.5},
            "inventory_turnover": {"low": 6, "median": 10, "high": 15},
            "asset_turnover": {"low": 1.5, "median": 2.5, "high": 4.0},
            "cash_runway_days": {"low": 45, "median": 90, "high": 150}
        },
        "Agriculture": {
            "current_ratio": {"low": 1.0, "median": 1.4, "high": 2.0},
            "quick_ratio": {"low": 0.6, "median": 0.9, "high": 1.2},
            "gross_margin": {"low": 15, "median": 25, "high": 40},
            "net_margin": {"low": 5, "median": 12, "high": 20},
            "debt_to_equity": {"low": 0.6, "median": 1.0, "high": 1.6},
            "inventory_turnover": {"low": 2, "median": 4, "high": 6},
            "asset_turnover": {"low": 0.5, "median": 0.8, "high": 1.2},
            "cash_runway_days": {"low": 90, "median": 180, "high": 300}
        },
        "Services": {
            "current_ratio": {"low": 1.3, "median": 1.8, "high": 2.5},
            "quick_ratio": {"low": 1.2, "median": 1.7, "high": 2.3},
            "gross_margin": {"low": 40, "median": 55, "high": 70},
            "net_margin": {"low": 8, "median": 15, "high": 25},
            "debt_to_equity": {"low": 0.3, "median": 0.6, "high": 1.0},
            "inventory_turnover": {"low": 0, "median": 0, "high": 0},
            "asset_turnover": {"low": 1.0, "median": 1.8, "high": 2.8},
            "cash_runway_days": {"low": 60, "median": 120, "high": 200}
        },
        "Logistics": {
            "current_ratio": {"low": 1.1, "median": 1.4, "high": 1.9},
            "quick_ratio": {"low": 0.9, "median": 1.2, "high": 1.6},
            "gross_margin": {"low": 15, "median": 25, "high": 35},
            "net_margin": {"low": 3, "median": 7, "high": 12},
            "debt_to_equity": {"low": 1.0, "median": 1.5, "high": 2.5},
            "inventory_turnover": {"low": 8, "median": 15, "high": 25},
            "asset_turnover": {"low": 1.2, "median": 1.8, "high": 2.5},
            "cash_runway_days": {"low": 45, "median": 90, "high": 150}
        },
        "E-commerce": {
            "current_ratio": {"low": 1.2, "median": 1.6, "high": 2.2},
            "quick_ratio": {"low": 0.8, "median": 1.2, "high": 1.8},
            "gross_margin": {"low": 20, "median": 35, "high": 50},
            "net_margin": {"low": 2, "median": 8, "high": 15},
            "debt_to_equity": {"low": 0.4, "median": 0.8, "high": 1.4},
            "inventory_turnover": {"low": 8, "median": 12, "high": 20},
            "asset_turnover": {"low": 1.8, "median": 3.0, "high": 5.0},
            "cash_runway_days": {"low": 60, "median": 120, "high": 200}
        }
    }
    
    def compare_to_industry(
        self, 
        metrics: Dict[str, Any], 
        industry: str
    ) -> Dict[str, Any]:
        """Compare company metrics to industry benchmarks"""
        benchmarks = self.BENCHMARKS.get(industry, self.BENCHMARKS["Services"])
        
        comparison = {}
        percentile_sum = 0
        percentile_count = 0
        
        for metric, benchmark in benchmarks.items():
            company_value = metrics.get(metric, 0)
            
            if benchmark["low"] == benchmark["high"] == 0:
                # Skip metrics not applicable (e.g., inventory for services)
                continue
            
            # Calculate percentile position
            percentile = self._calculate_percentile(
                company_value, 
                benchmark["low"], 
                benchmark["median"], 
                benchmark["high"]
            )
            
            # Determine status
            if company_value >= benchmark["high"]:
                status = "excellent"
            elif company_value >= benchmark["median"]:
                status = "good"
            elif company_value >= benchmark["low"]:
                status = "average"
            else:
                status = "below_average"
            
            comparison[metric] = {
                "company_value": round(company_value, 2),
                "industry_low": benchmark["low"],
                "industry_median": benchmark["median"],
                "industry_high": benchmark["high"],
                "percentile": percentile,
                "status": status
            }
            
            percentile_sum += percentile
            percentile_count += 1
        
        # Calculate overall percentile
        overall_percentile = percentile_sum / percentile_count if percentile_count > 0 else 50
        
        return {
            "industry": industry,
            "percentile": round(overall_percentile, 1),
            "comparison": comparison,
            "summary": self._generate_benchmark_summary(comparison, overall_percentile)
        }
    
    def _calculate_percentile(
        self, 
        value: float, 
        low: float, 
        median: float, 
        high: float
    ) -> float:
        """Calculate approximate percentile position"""
        if value <= low:
            # Below 25th percentile
            return min(25, (value / low) * 25) if low > 0 else 0
        elif value <= median:
            # Between 25th and 50th percentile
            return 25 + ((value - low) / (median - low)) * 25
        elif value <= high:
            # Between 50th and 75th percentile
            return 50 + ((value - median) / (high - median)) * 25
        else:
            # Above 75th percentile
            return min(100, 75 + ((value - high) / high) * 25)
    
    def _generate_benchmark_summary(
        self, 
        comparison: Dict[str, Any], 
        overall_percentile: float
    ) -> Dict[str, Any]:
        """Generate summary of benchmark comparison"""
        strengths = []
        weaknesses = []
        
        for metric, data in comparison.items():
            if data["status"] in ["excellent", "good"]:
                strengths.append({
                    "metric": metric,
                    "value": data["company_value"],
                    "percentile": data["percentile"]
                })
            elif data["status"] == "below_average":
                weaknesses.append({
                    "metric": metric,
                    "value": data["company_value"],
                    "percentile": data["percentile"]
                })
        
        # Sort by percentile
        strengths.sort(key=lambda x: x["percentile"], reverse=True)
        weaknesses.sort(key=lambda x: x["percentile"])
        
        return {
            "overall_position": self._get_position_label(overall_percentile),
            "top_strengths": strengths[:3],
            "areas_for_improvement": weaknesses[:3]
        }
    
    def _get_position_label(self, percentile: float) -> str:
        """Get label for percentile position"""
        if percentile >= 75:
            return "Top Quartile (Industry Leader)"
        elif percentile >= 50:
            return "Above Average"
        elif percentile >= 25:
            return "Below Average"
        else:
            return "Bottom Quartile (Needs Attention)"
