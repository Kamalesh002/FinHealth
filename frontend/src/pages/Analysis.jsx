import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { companyAPI, analysisAPI } from '../services/api';
import HealthScoreCard from '../components/HealthScoreCard';
import MetricChart from '../components/MetricChart';
import ChatInterface from '../components/ChatInterface';
import ProductRecommendations from '../components/ProductRecommendations';
import {
    ArrowLeft, RefreshCw, Download, TrendingUp, TrendingDown,
    AlertTriangle, Lightbulb, BarChart3, Target, CreditCard
} from 'lucide-react';

function Analysis() {
    const { companyId } = useParams();
    const { t } = useTranslation();
    const navigate = useNavigate();

    const [company, setCompany] = useState(null);
    const [healthScore, setHealthScore] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('overview');
    const [recalculating, setRecalculating] = useState(false);
    const [downloading, setDownloading] = useState(false);

    useEffect(() => {
        if (companyId) {
            loadData();
        }
    }, [companyId]);

    const loadData = async () => {
        try {
            const [companiesRes, scoreRes] = await Promise.all([
                companyAPI.getAll(),
                analysisAPI.getHealthScore(companyId)
            ]);

            const currentCompany = companiesRes.data.find(c => c.id === parseInt(companyId));
            setCompany(currentCompany);
            setHealthScore(scoreRes.data);
        } catch (error) {
            console.error('Failed to load analysis:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleRecalculate = async () => {
        setRecalculating(true);
        try {
            const response = await analysisAPI.getHealthScore(companyId, true);
            setHealthScore(response.data);
        } catch (error) {
            console.error('Failed to recalculate:', error);
        } finally {
            setRecalculating(false);
        }
    };

    const handleDownloadReport = async () => {
        setDownloading(true);
        try {
            const response = await analysisAPI.downloadReport(companyId);
            const blob = new Blob([response.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${company?.name || 'Company'}_Financial_Health_Report.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Failed to download report:', error);
            alert('Failed to generate report. Please try again.');
        } finally {
            setDownloading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center" style={{ height: '60vh' }}>
                <div className="loader"></div>
            </div>
        );
    }

    if (!healthScore) {
        return (
            <div className="no-data-page">
                <BarChart3 size={64} className="no-data-icon" />
                <h2>No Analysis Available</h2>
                <p>Upload and validate financial documents to see your analysis.</p>
                <button className="btn btn-primary" onClick={() => navigate('/upload')}>
                    Upload Documents
                </button>
            </div>
        );
    }

    const tabs = [
        { id: 'overview', label: t('analysis.overview'), icon: BarChart3 },
        { id: 'benchmark', label: t('analysis.benchmark'), icon: Target },
        { id: 'risks', label: t('analysis.risks'), icon: AlertTriangle },
        { id: 'recommendations', label: t('analysis.recommendations'), icon: Lightbulb },
        { id: 'financing', label: 'Financing Options', icon: CreditCard },
    ];

    // Prepare chart data
    const scoreBreakdownData = [
        { name: 'Liquidity', value: healthScore.liquidity_score },
        { name: 'Profitability', value: healthScore.profitability_score },
        { name: 'Solvency', value: healthScore.solvency_score },
        { name: 'Efficiency', value: healthScore.efficiency_score },
        { name: 'Cash Flow', value: healthScore.cash_flow_score }
    ];

    const benchmarkData = healthScore.benchmark_data?.comparison
        ? Object.entries(healthScore.benchmark_data.comparison).slice(0, 6).map(([key, data]) => ({
            name: key.replace(/_/g, ' '),
            company: data.company_value,
            industry: data.industry_median
        }))
        : [];

    const forecastData = healthScore.forecast_data?.revenue_forecast?.monthly_breakdown || [];

    return (
        <div className="analysis-page">
            {/* Header */}
            <div className="analysis-header">
                <div className="header-left">
                    <button className="btn btn-secondary back-btn" onClick={() => navigate('/dashboard')}>
                        <ArrowLeft size={18} />
                    </button>
                    <div>
                        <h1>{company?.name || 'Company'}</h1>
                        <p className="text-secondary">{company?.industry}</p>
                    </div>
                </div>
                <div className="header-actions">
                    <button
                        className="btn btn-secondary"
                        onClick={handleRecalculate}
                        disabled={recalculating}
                    >
                        <RefreshCw size={16} className={recalculating ? 'animate-spin' : ''} />
                        Recalculate
                    </button>
                    <button
                        className="btn btn-primary"
                        onClick={handleDownloadReport}
                        disabled={downloading}
                    >
                        <Download size={16} className={downloading ? 'animate-pulse' : ''} />
                        {downloading ? 'Generating...' : 'Export Report'}
                    </button>
                </div>
            </div>

            {/* Tabs */}
            <div className="analysis-tabs">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        className={`tab ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        <tab.icon size={16} />
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Content Grid */}
            <div className="analysis-grid">
                {/* Main Content */}
                <div className="analysis-main">
                    {activeTab === 'overview' && (
                        <>
                            {/* Score Cards Row */}
                            <div className="score-grid">
                                <HealthScoreCard
                                    score={healthScore.overall_score}
                                    grade={healthScore.score_grade}
                                    riskLevel={healthScore.risk_level}
                                />
                                <MetricChart
                                    type="bar"
                                    title="Score Breakdown"
                                    data={scoreBreakdownData}
                                    height={200}
                                />
                            </div>

                            {/* Summary */}
                            <div className="summary-card">
                                <h3>AI Summary</h3>
                                <p>{healthScore.summary}</p>
                            </div>

                            {/* Key Metrics */}
                            <div className="metrics-grid">
                                <div className="metric-card">
                                    <span className="metric-label">Current Ratio</span>
                                    <span className="metric-value">{healthScore.metrics?.current_ratio?.toFixed(2)}</span>
                                </div>
                                <div className="metric-card">
                                    <span className="metric-label">Net Margin</span>
                                    <span className="metric-value">{healthScore.metrics?.net_margin?.toFixed(1)}%</span>
                                </div>
                                <div className="metric-card">
                                    <span className="metric-label">Cash Runway</span>
                                    <span className="metric-value">{healthScore.metrics?.cash_runway_days} days</span>
                                </div>
                                <div className="metric-card">
                                    <span className="metric-label">Debt/Equity</span>
                                    <span className="metric-value">{healthScore.metrics?.debt_to_equity?.toFixed(2)}</span>
                                </div>
                            </div>

                            {/* Forecast Chart */}
                            {forecastData.length > 0 && (
                                <MetricChart
                                    type="line"
                                    title="Revenue Forecast (12 Months)"
                                    data={forecastData.map(f => ({ name: `M${f.month}`, value: f.projected_revenue }))}
                                    height={250}
                                />
                            )}
                        </>
                    )}

                    {activeTab === 'benchmark' && (
                        <>
                            <div className="benchmark-summary">
                                <div className="percentile-badge">
                                    <span className="percentile-value">{healthScore.industry_percentile?.toFixed(0)}th</span>
                                    <span className="percentile-label">Percentile</span>
                                </div>
                                <div className="benchmark-text">
                                    <h3>{healthScore.benchmark_data?.summary?.overall_position}</h3>
                                    <p>Compared to other {company?.industry} businesses</p>
                                </div>
                            </div>

                            {benchmarkData.length > 0 && (
                                <MetricChart
                                    type="multiBar"
                                    title="Your Metrics vs Industry Median"
                                    data={benchmarkData}
                                    height={300}
                                />
                            )}

                            {/* Strengths & Weaknesses */}
                            <div className="sw-grid">
                                <div className="sw-card strengths">
                                    <h4><TrendingUp size={18} /> Strengths</h4>
                                    <ul>
                                        {healthScore.benchmark_data?.summary?.top_strengths?.map((s, i) => (
                                            <li key={i}>{s.metric}: {s.percentile?.toFixed(0)}th percentile</li>
                                        ))}
                                    </ul>
                                </div>
                                <div className="sw-card weaknesses">
                                    <h4><TrendingDown size={18} /> Areas to Improve</h4>
                                    <ul>
                                        {healthScore.benchmark_data?.summary?.areas_for_improvement?.map((w, i) => (
                                            <li key={i}>{w.metric}: {w.percentile?.toFixed(0)}th percentile</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </>
                    )}

                    {activeTab === 'risks' && (
                        <div className="risks-list">
                            {healthScore.risk_factors?.length > 0 ? (
                                healthScore.risk_factors.map((risk, idx) => (
                                    <div key={idx} className={`risk-card ${risk.severity}`}>
                                        <div className="risk-header">
                                            <AlertTriangle size={20} />
                                            <h4>{risk.name}</h4>
                                            <span className={`risk-pill ${risk.severity}`}>{risk.severity}</span>
                                        </div>
                                        <p>{risk.description}</p>
                                        <span className="risk-indicator">{risk.indicator}</span>
                                    </div>
                                ))
                            ) : (
                                <div className="no-risks">
                                    <TrendingUp size={48} />
                                    <h3>No Major Risks Identified</h3>
                                    <p>Your financial health looks good!</p>
                                </div>
                            )}
                        </div>
                    )}

                    {activeTab === 'recommendations' && (
                        <div className="recommendations-list">
                            {healthScore.recommendations?.map((rec, idx) => (
                                <div key={idx} className={`recommendation-card priority-${rec.priority}`}>
                                    <div className="rec-header">
                                        <Lightbulb size={20} />
                                        <h4>{rec.title}</h4>
                                        <span className={`priority-badge ${rec.priority}`}>{rec.priority}</span>
                                    </div>
                                    <p>{rec.description}</p>
                                    {rec.expected_impact && (
                                        <div className="expected-impact">
                                            <strong>Expected Impact:</strong> {rec.expected_impact}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}

                    {activeTab === 'financing' && (
                        <ProductRecommendations companyId={parseInt(companyId)} />
                    )}
                </div>

                {/* Sidebar - Chat */}
                <div className="analysis-sidebar">
                    <ChatInterface companyId={parseInt(companyId)} />
                </div>
            </div>

            <style>{`
        .analysis-page h1 {
          font-size: var(--font-size-2xl);
          font-weight: 700;
        }

        .analysis-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: var(--spacing-xl);
        }

        .header-left {
          display: flex;
          align-items: center;
          gap: var(--spacing-md);
        }

        .back-btn {
          padding: var(--spacing-sm);
        }

        .header-actions {
          display: flex;
          gap: var(--spacing-md);
        }

        .analysis-tabs {
          display: flex;
          gap: var(--spacing-sm);
          margin-bottom: var(--spacing-xl);
          border-bottom: 1px solid var(--border);
          padding-bottom: var(--spacing-sm);
        }

        .tab {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          padding: var(--spacing-sm) var(--spacing-md);
          background: transparent;
          border: none;
          color: var(--text-secondary);
          cursor: pointer;
          border-radius: var(--radius-md);
          transition: all var(--transition-fast);
        }

        .tab:hover {
          color: var(--text-primary);
          background: var(--bg-card);
        }

        .tab.active {
          color: var(--primary);
          background: rgba(99, 102, 241, 0.1);
        }

        .analysis-grid {
          display: grid;
          grid-template-columns: 1fr 400px;
          gap: var(--spacing-xl);
        }

        .analysis-main {
          display: flex;
          flex-direction: column;
          gap: var(--spacing-lg);
        }

        .score-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: var(--spacing-lg);
        }

        .summary-card {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--spacing-lg);
          border: 1px solid var(--border);
        }

        .summary-card h3 {
          margin-bottom: var(--spacing-md);
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
        }

        .summary-card p {
          color: var(--text-secondary);
          line-height: 1.7;
        }

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: var(--spacing-md);
        }

        .metric-card {
          background: var(--bg-card);
          border-radius: var(--radius-md);
          padding: var(--spacing-md);
          border: 1px solid var(--border);
          display: flex;
          flex-direction: column;
          gap: var(--spacing-xs);
        }

        .metric-label {
          font-size: var(--font-size-sm);
          color: var(--text-muted);
        }

        .metric-value {
          font-size: var(--font-size-xl);
          font-weight: 600;
        }

        .benchmark-summary {
          display: flex;
          align-items: center;
          gap: var(--spacing-xl);
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--spacing-xl);
          border: 1px solid var(--border);
          margin-bottom: var(--spacing-lg);
        }

        .percentile-badge {
          width: 100px;
          height: 100px;
          border-radius: 50%;
          background: var(--gradient-primary);
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }

        .percentile-value {
          font-size: var(--font-size-2xl);
          font-weight: 700;
        }

        .percentile-label {
          font-size: var(--font-size-xs);
          opacity: 0.8;
        }

        .sw-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: var(--spacing-lg);
          margin-top: var(--spacing-lg);
        }

        .sw-card {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--spacing-lg);
          border: 1px solid var(--border);
        }

        .sw-card h4 {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          margin-bottom: var(--spacing-md);
        }

        .sw-card.strengths h4 { color: var(--success); }
        .sw-card.weaknesses h4 { color: var(--warning); }

        .sw-card ul {
          list-style: none;
        }

        .sw-card li {
          padding: var(--spacing-xs) 0;
          font-size: var(--font-size-sm);
          color: var(--text-secondary);
        }

        .risks-list, .recommendations-list {
          display: flex;
          flex-direction: column;
          gap: var(--spacing-md);
        }

        .risk-card, .recommendation-card {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--spacing-lg);
          border: 1px solid var(--border);
        }

        .risk-card.critical { border-left: 3px solid var(--danger); }
        .risk-card.high { border-left: 3px solid var(--warning); }
        .risk-card.medium { border-left: 3px solid var(--info); }

        .risk-header, .rec-header {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          margin-bottom: var(--spacing-sm);
        }

        .risk-header svg { color: var(--warning); }
        .rec-header svg { color: var(--primary); }

        .risk-header h4, .rec-header h4 {
          flex: 1;
        }

        .risk-indicator {
          display: inline-block;
          margin-top: var(--spacing-sm);
          padding: var(--spacing-xs) var(--spacing-sm);
          background: var(--bg-dark);
          border-radius: var(--radius-sm);
          font-size: var(--font-size-sm);
          color: var(--text-muted);
        }

        .priority-badge {
          padding: var(--spacing-xs) var(--spacing-sm);
          border-radius: var(--radius-full);
          font-size: var(--font-size-xs);
          font-weight: 600;
          text-transform: uppercase;
        }

        .priority-badge.high { background: rgba(239, 68, 68, 0.2); color: var(--danger); }
        .priority-badge.medium { background: rgba(245, 158, 11, 0.2); color: var(--warning); }
        .priority-badge.low { background: rgba(16, 185, 129, 0.2); color: var(--success); }

        .expected-impact {
          margin-top: var(--spacing-md);
          padding: var(--spacing-sm);
          background: rgba(99, 102, 241, 0.1);
          border-radius: var(--radius-md);
          font-size: var(--font-size-sm);
        }

        .no-risks, .no-data-page {
          text-align: center;
          padding: var(--spacing-2xl);
          color: var(--text-secondary);
        }

        .no-risks svg, .no-data-page svg {
          color: var(--success);
          margin-bottom: var(--spacing-md);
        }

        @media (max-width: 1200px) {
          .analysis-grid { grid-template-columns: 1fr; }
          .score-grid { grid-template-columns: 1fr; }
          .metrics-grid { grid-template-columns: repeat(2, 1fr); }
          .sw-grid { grid-template-columns: 1fr; }
        }
      `}</style>
        </div>
    );
}

export default Analysis;
