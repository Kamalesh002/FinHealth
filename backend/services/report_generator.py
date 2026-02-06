"""
Report Generator - Creates investor-ready PDF reports
"""
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Circle, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart


class ReportGenerator:
    """Generate professional financial health reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='Title_Custom',
            parent=self.styles['Title'],
            fontSize=28,
            spaceAfter=30,
            textColor=colors.HexColor('#1E3A8A')
        ))
        
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1F2937'),
            spaceBefore=20,
            spaceAfter=10,
            borderPadding=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyText_Custom',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            leading=16
        ))
        
        self.styles.add(ParagraphStyle(
            name='HighlightBox',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.white,
            backColor=colors.HexColor('#10B981'),
            borderPadding=10
        ))
    
    def generate_health_report(
        self,
        company_name: str,
        industry: str,
        health_score: Dict[str, Any],
        product_recommendations: Optional[List[Dict]] = None
    ) -> BytesIO:
        """Generate a complete financial health report PDF"""
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        story = []
        
        # Title Page
        story.extend(self._create_title_page(company_name, industry, health_score))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._create_executive_summary(health_score))
        story.append(Spacer(1, 20))
        
        # Score Breakdown
        story.extend(self._create_score_breakdown(health_score))
        story.append(Spacer(1, 20))
        
        # Key Metrics
        story.extend(self._create_metrics_section(health_score.get('metrics', {})))
        story.append(PageBreak())
        
        # Risk Analysis
        story.extend(self._create_risk_section(health_score.get('risk_factors', [])))
        story.append(Spacer(1, 20))
        
        # Recommendations
        story.extend(self._create_recommendations_section(health_score.get('recommendations', [])))
        
        # Financing Options
        if product_recommendations:
            story.append(PageBreak())
            story.extend(self._create_financing_section(product_recommendations))
        
        # Forecast
        if health_score.get('forecast_data'):
            story.append(PageBreak())
            story.extend(self._create_forecast_section(health_score.get('forecast_data', {})))
        
        # Footer with disclaimer
        story.append(Spacer(1, 30))
        story.extend(self._create_disclaimer())
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _create_title_page(self, company_name: str, industry: str, health_score: Dict) -> List:
        """Create the title page"""
        elements = []
        
        elements.append(Spacer(1, 100))
        
        # Title
        elements.append(Paragraph(
            "Financial Health Report",
            self.styles['Title_Custom']
        ))
        
        # Company name
        elements.append(Paragraph(
            f"<b>{company_name}</b>",
            ParagraphStyle(
                'CompanyName',
                parent=self.styles['Normal'],
                fontSize=20,
                textColor=colors.HexColor('#374151'),
                spaceAfter=10
            )
        ))
        
        # Industry
        elements.append(Paragraph(
            f"Industry: {industry}",
            self.styles['Subtitle']
        ))
        
        elements.append(Spacer(1, 40))
        
        # Health Score Display
        score = health_score.get('overall_score', 0)
        grade = health_score.get('score_grade', 'N/A')
        risk = health_score.get('risk_level', 'Unknown')
        
        score_color = self._get_score_color(score)
        
        score_table = Table(
            [[
                Paragraph(f"<font size='48' color='{score_color}'><b>{score:.0f}</b></font>", self.styles['Normal']),
                Paragraph(f"<font size='24'>Grade: <b>{grade}</b></font><br/><font size='12'>Risk Level: {risk}</font>", self.styles['Normal'])
            ]],
            colWidths=[150, 200]
        )
        score_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#E5E7EB')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
            ('LEFTPADDING', (0, 0), (-1, -1), 30),
            ('RIGHTPADDING', (0, 0), (-1, -1), 30),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ]))
        elements.append(score_table)
        
        elements.append(Spacer(1, 60))
        
        # Generated date
        elements.append(Paragraph(
            f"Report Generated: {datetime.now().strftime('%B %d, %Y')}",
            self.styles['Subtitle']
        ))
        
        return elements
    
    def _create_executive_summary(self, health_score: Dict) -> List:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
        elements.append(Spacer(1, 10))
        
        summary = health_score.get('summary', 'No summary available.')
        elements.append(Paragraph(summary, self.styles['BodyText_Custom']))
        
        return elements
    
    def _create_score_breakdown(self, health_score: Dict) -> List:
        """Create score breakdown table"""
        elements = []
        
        elements.append(Paragraph("Score Breakdown", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
        elements.append(Spacer(1, 10))
        
        # Score data
        scores = [
            ['Category', 'Score', 'Rating'],
            ['Liquidity', f"{health_score.get('liquidity_score', 0):.0f}/100", self._get_rating(health_score.get('liquidity_score', 0))],
            ['Profitability', f"{health_score.get('profitability_score', 0):.0f}/100", self._get_rating(health_score.get('profitability_score', 0))],
            ['Solvency', f"{health_score.get('solvency_score', 0):.0f}/100", self._get_rating(health_score.get('solvency_score', 0))],
            ['Efficiency', f"{health_score.get('efficiency_score', 0):.0f}/100", self._get_rating(health_score.get('efficiency_score', 0))],
            ['Cash Flow', f"{health_score.get('cash_flow_score', 0):.0f}/100", self._get_rating(health_score.get('cash_flow_score', 0))],
        ]
        
        table = Table(scores, colWidths=[200, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F9FAFB')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        return elements
    
    def _create_metrics_section(self, metrics: Dict) -> List:
        """Create key metrics section"""
        elements = []
        
        elements.append(Paragraph("Key Financial Metrics", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
        elements.append(Spacer(1, 10))
        
        metric_data = [
            ['Metric', 'Value', 'Status'],
            ['Current Ratio', f"{metrics.get('current_ratio', 0):.2f}", '✓ Healthy' if metrics.get('current_ratio', 0) >= 1.5 else '⚠ Monitor'],
            ['Net Profit Margin', f"{metrics.get('net_margin', 0):.1f}%", '✓ Healthy' if metrics.get('net_margin', 0) >= 5 else '⚠ Monitor'],
            ['Debt-to-Equity', f"{metrics.get('debt_to_equity', 0):.2f}", '✓ Healthy' if metrics.get('debt_to_equity', 0) <= 1.5 else '⚠ Monitor'],
            ['Cash Runway', f"{metrics.get('cash_runway_days', 0)} days", '✓ Healthy' if metrics.get('cash_runway_days', 0) >= 90 else '⚠ Monitor'],
            ['Working Capital Cycle', f"{metrics.get('working_capital_cycle', 0)} days", '✓ Healthy' if metrics.get('working_capital_cycle', 0) <= 60 else '⚠ Monitor'],
            ['ROE', f"{metrics.get('roe', 0):.1f}%", '✓ Healthy' if metrics.get('roe', 0) >= 10 else '⚠ Monitor'],
        ]
        
        table = Table(metric_data, colWidths=[180, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        return elements
    
    def _create_risk_section(self, risks: List[Dict]) -> List:
        """Create risk analysis section"""
        elements = []
        
        elements.append(Paragraph("Risk Analysis", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
        elements.append(Spacer(1, 10))
        
        if not risks:
            elements.append(Paragraph(
                "✅ No major financial risks identified. Your financial health looks stable.",
                self.styles['BodyText_Custom']
            ))
            return elements
        
        for risk in risks[:5]:  # Limit to top 5 risks
            severity = risk.get('severity', 'medium')
            color = {'critical': '#DC2626', 'high': '#F59E0B', 'medium': '#3B82F6'}.get(severity, '#6B7280')
            
            elements.append(Paragraph(
                f"<font color='{color}'>●</font> <b>{risk.get('name', 'Risk')}</b> ({severity.upper()})",
                self.styles['BodyText_Custom']
            ))
            elements.append(Paragraph(
                f"&nbsp;&nbsp;&nbsp;{risk.get('description', '')}",
                ParagraphStyle('RiskDesc', parent=self.styles['BodyText_Custom'], fontSize=10, textColor=colors.HexColor('#6B7280'))
            ))
        
        return elements
    
    def _create_recommendations_section(self, recommendations: List[Dict]) -> List:
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("Recommendations", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
        elements.append(Spacer(1, 10))
        
        if not recommendations:
            elements.append(Paragraph("No specific recommendations at this time.", self.styles['BodyText_Custom']))
            return elements
        
        for idx, rec in enumerate(recommendations[:5], 1):
            priority = rec.get('priority', 'medium')
            elements.append(Paragraph(
                f"<b>{idx}. {rec.get('title', 'Recommendation')}</b> [{priority.upper()}]",
                self.styles['BodyText_Custom']
            ))
            elements.append(Paragraph(
                f"&nbsp;&nbsp;&nbsp;{rec.get('description', '')}",
                ParagraphStyle('RecDesc', parent=self.styles['BodyText_Custom'], fontSize=10, textColor=colors.HexColor('#6B7280'))
            ))
            if rec.get('expected_impact'):
                elements.append(Paragraph(
                    f"&nbsp;&nbsp;&nbsp;<i>Expected Impact: {rec.get('expected_impact')}</i>",
                    ParagraphStyle('RecImpact', parent=self.styles['BodyText_Custom'], fontSize=9, textColor=colors.HexColor('#10B981'))
                ))
            elements.append(Spacer(1, 5))
        
        return elements
    
    def _create_financing_section(self, products: List[Dict]) -> List:
        """Create financing options section"""
        elements = []
        
        elements.append(Paragraph("Recommended Financing Options", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
        elements.append(Spacer(1, 10))
        
        elements.append(Paragraph(
            "Based on your financial profile, the following financing options may be suitable:",
            self.styles['BodyText_Custom']
        ))
        
        for product in products[:3]:
            p = product.get('product', product)
            elements.append(Paragraph(
                f"<b>💳 {p.get('name', 'Product')}</b>",
                self.styles['BodyText_Custom']
            ))
            elements.append(Paragraph(
                f"&nbsp;&nbsp;&nbsp;{p.get('description', '')}",
                ParagraphStyle('ProdDesc', parent=self.styles['BodyText_Custom'], fontSize=10, textColor=colors.HexColor('#6B7280'))
            ))
            elements.append(Paragraph(
                f"&nbsp;&nbsp;&nbsp;Interest: {p.get('interest_rate_range', 'N/A')} | Amount: {p.get('loan_amount_range', 'N/A')}",
                ParagraphStyle('ProdDetail', parent=self.styles['BodyText_Custom'], fontSize=9, textColor=colors.HexColor('#374151'))
            ))
            elements.append(Spacer(1, 8))
        
        return elements
    
    def _create_forecast_section(self, forecast: Dict) -> List:
        """Create forecast section"""
        elements = []
        
        elements.append(Paragraph("12-Month Financial Forecast", self.styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
        elements.append(Spacer(1, 10))
        
        revenue_forecast = forecast.get('revenue_forecast', {})
        if revenue_forecast:
            elements.append(Paragraph(
                f"<b>Projected Revenue:</b> ₹{revenue_forecast.get('total_projected', 0):,.0f}",
                self.styles['BodyText_Custom']
            ))
            elements.append(Paragraph(
                f"<b>Growth Rate:</b> {revenue_forecast.get('growth_rate', 0):.1f}%",
                self.styles['BodyText_Custom']
            ))
        
        cash_flow = forecast.get('cash_flow_forecast', {})
        if cash_flow:
            elements.append(Paragraph(
                f"<b>Projected Net Cash Flow:</b> ₹{cash_flow.get('total_net_flow', 0):,.0f}",
                self.styles['BodyText_Custom']
            ))
        
        return elements
    
    def _create_disclaimer(self) -> List:
        """Create disclaimer section"""
        elements = []
        
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
        elements.append(Spacer(1, 10))
        
        elements.append(Paragraph(
            "<b>Disclaimer:</b> This report is generated based on the financial data provided and is for informational purposes only. "
            "It should not be considered as financial advice. Please consult with a qualified financial advisor before making any business decisions.",
            ParagraphStyle('Disclaimer', parent=self.styles['Normal'], fontSize=8, textColor=colors.HexColor('#9CA3AF'))
        ))
        
        elements.append(Paragraph(
            f"Generated by SME Financial Health Platform | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            ParagraphStyle('Footer', parent=self.styles['Normal'], fontSize=8, textColor=colors.HexColor('#9CA3AF'), alignment=TA_CENTER)
        ))
        
        return elements
    
    def _get_score_color(self, score: float) -> str:
        """Get color based on score"""
        if score >= 80:
            return '#10B981'
        elif score >= 60:
            return '#3B82F6'
        elif score >= 40:
            return '#F59E0B'
        else:
            return '#EF4444'
    
    def _get_rating(self, score: float) -> str:
        """Get rating text based on score"""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        else:
            return 'Needs Attention'

