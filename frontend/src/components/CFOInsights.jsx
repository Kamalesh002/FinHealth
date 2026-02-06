import { useState, useEffect } from 'react';
import { analysisAPI } from '../services/api';
import { Lightbulb, TrendingUp, DollarSign, Scale, Droplet, RefreshCw } from 'lucide-react';

function CFOInsights({ companyId }) {
    const [insights, setInsights] = useState([]);
    const [loading, setLoading] = useState(true);
    const [companyName, setCompanyName] = useState('');

    useEffect(() => {
        if (companyId) {
            loadInsights();
        }
    }, [companyId]);

    const loadInsights = async () => {
        try {
            const response = await analysisAPI.getCFOInsights(companyId);
            if (response.data.has_data) {
                setInsights(response.data.insights || []);
                setCompanyName(response.data.company_name || '');
            }
        } catch (error) {
            console.error('Failed to load CFO insights:', error);
        } finally {
            setLoading(false);
        }
    };

    const getCategoryIcon = (category) => {
        switch (category) {
            case 'Overall Health':
                return <TrendingUp size={20} />;
            case 'Cash Position':
                return <DollarSign size={20} />;
            case 'Debt Health':
                return <Scale size={20} />;
            case 'Profitability':
                return <TrendingUp size={20} />;
            case 'Bill Paying Ability':
                return <Droplet size={20} />;
            case 'Cash Efficiency':
                return <RefreshCw size={20} />;
            default:
                return <Lightbulb size={20} />;
        }
    };

    const getColorClass = (color) => {
        switch (color) {
            case 'success':
                return 'insight-success';
            case 'warning':
                return 'insight-warning';
            case 'danger':
                return 'insight-danger';
            case 'info':
                return 'insight-info';
            default:
                return 'insight-default';
        }
    };

    if (loading) {
        return (
            <div className="cfo-insights-loading">
                <div className="loader"></div>
            </div>
        );
    }

    if (insights.length === 0) {
        return null;
    }

    return (
        <div className="cfo-insights-container animate-fadeIn">
            <div className="cfo-header">
                <div className="cfo-title-section">
                    <Lightbulb size={24} className="cfo-icon" />
                    <div>
                        <h3 className="cfo-title">CFO Insights</h3>
                        <p className="cfo-subtitle">Plain-language financial analysis</p>
                    </div>
                </div>
            </div>

            <div className="insights-grid">
                {insights.map((insight, index) => (
                    <div
                        key={index}
                        className={`insight-card ${getColorClass(insight.color)}`}
                    >
                        <div className="insight-header">
                            <div className="insight-icon">
                                {getCategoryIcon(insight.category)}
                            </div>
                            <div className="insight-meta">
                                <span className="insight-category">{insight.category}</span>
                                <span className="insight-metric">{insight.metric_name}</span>
                            </div>
                            <div className="insight-value">
                                {insight.metric_value}
                            </div>
                        </div>
                        <p className="insight-interpretation">
                            {insight.interpretation}
                        </p>
                    </div>
                ))}
            </div>

            <style>{`
                .cfo-insights-container {
                    background: var(--bg-card);
                    border-radius: var(--radius-xl);
                    border: 1px solid var(--border);
                    overflow: hidden;
                    margin-bottom: var(--spacing-xl);
                }

                .cfo-header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: var(--spacing-lg);
                    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                    color: white;
                }

                .cfo-title-section {
                    display: flex;
                    align-items: center;
                    gap: var(--spacing-md);
                }

                .cfo-icon {
                    color: #fcd34d;
                }

                .cfo-title {
                    font-size: var(--font-size-lg);
                    font-weight: 600;
                    margin: 0;
                }

                .cfo-subtitle {
                    font-size: var(--font-size-sm);
                    opacity: 0.9;
                    margin: 0;
                }

                .insights-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                    gap: var(--spacing-md);
                    padding: var(--spacing-lg);
                }

                .insight-card {
                    padding: var(--spacing-md);
                    border-radius: var(--radius-lg);
                    border: 1px solid var(--border);
                    transition: all var(--transition-fast);
                }

                .insight-card:hover {
                    transform: translateY(-2px);
                    box-shadow: var(--shadow-md);
                }

                .insight-success {
                    border-left: 4px solid #10b981;
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.02) 100%);
                }

                .insight-warning {
                    border-left: 4px solid #f59e0b;
                    background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(245, 158, 11, 0.02) 100%);
                }

                .insight-danger {
                    border-left: 4px solid #ef4444;
                    background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.02) 100%);
                }

                .insight-info {
                    border-left: 4px solid #3b82f6;
                    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(59, 130, 246, 0.02) 100%);
                }

                .insight-default {
                    border-left: 4px solid #94a3b8;
                    background: var(--bg-secondary);
                }

                .insight-header {
                    display: flex;
                    align-items: flex-start;
                    gap: var(--spacing-sm);
                    margin-bottom: var(--spacing-sm);
                }

                .insight-icon {
                    padding: var(--spacing-xs);
                    border-radius: var(--radius-md);
                    background: rgba(0, 0, 0, 0.05);
                }

                .insight-success .insight-icon { color: #10b981; }
                .insight-warning .insight-icon { color: #f59e0b; }
                .insight-danger .insight-icon { color: #ef4444; }
                .insight-info .insight-icon { color: #3b82f6; }

                .insight-meta {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                }

                .insight-category {
                    font-size: var(--font-size-xs);
                    color: var(--text-muted);
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }

                .insight-metric {
                    font-size: var(--font-size-sm);
                    font-weight: 600;
                    color: var(--text-primary);
                }

                .insight-value {
                    font-size: var(--font-size-xl);
                    font-weight: 700;
                    color: var(--text-primary);
                }

                .insight-interpretation {
                    font-size: var(--font-size-sm);
                    color: var(--text-secondary);
                    line-height: 1.5;
                    margin: 0;
                }

                .cfo-insights-loading {
                    display: flex;
                    justify-content: center;
                    padding: var(--spacing-xl);
                }

                @media (max-width: 768px) {
                    .insights-grid {
                        grid-template-columns: 1fr;
                    }
                }
            `}</style>
        </div>
    );
}

export default CFOInsights;
