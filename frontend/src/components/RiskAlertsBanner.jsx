import { useState, useEffect } from 'react';
import { analysisAPI } from '../services/api';
import { AlertTriangle, AlertCircle, CheckCircle, TrendingDown, Zap } from 'lucide-react';

function RiskAlertsBanner({ companyId }) {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [expanded, setExpanded] = useState(false);

    useEffect(() => {
        if (companyId) {
            loadAlerts();
        }
    }, [companyId]);

    const loadAlerts = async () => {
        try {
            const response = await analysisAPI.getRiskAlerts(companyId);
            if (response.data.has_data) {
                setAlerts(response.data.alerts || []);
            }
        } catch (error) {
            console.error('Failed to load risk alerts:', error);
        } finally {
            setLoading(false);
        }
    };

    const getAlertIcon = (type) => {
        switch (type) {
            case 'critical':
                return <AlertCircle size={20} />;
            case 'warning':
                return <AlertTriangle size={20} />;
            case 'success':
                return <CheckCircle size={20} />;
            default:
                return <Zap size={20} />;
        }
    };

    const getAlertClass = (type) => {
        switch (type) {
            case 'critical':
                return 'alert-critical';
            case 'warning':
                return 'alert-warning';
            case 'success':
                return 'alert-success';
            default:
                return 'alert-info';
        }
    };

    if (loading) {
        return null;
    }

    if (alerts.length === 0) {
        return null;
    }

    const criticalAlerts = alerts.filter(a => a.type === 'critical');
    const warningAlerts = alerts.filter(a => a.type === 'warning');
    const displayAlerts = expanded ? alerts : alerts.slice(0, 3);

    return (
        <div className="risk-alerts-container animate-fadeIn">
            {/* Summary Banner */}
            <div className="risk-summary-banner">
                <div className="risk-summary-content">
                    <Zap size={24} className="risk-icon" />
                    <div className="risk-summary-text">
                        <span className="risk-title">Smart Risk Alerts</span>
                        <span className="risk-count">
                            {criticalAlerts.length > 0 && (
                                <span className="critical-badge">{criticalAlerts.length} Critical</span>
                            )}
                            {warningAlerts.length > 0 && (
                                <span className="warning-badge">{warningAlerts.length} Warning</span>
                            )}
                            {alerts.filter(a => a.type === 'success').length > 0 && (
                                <span className="success-badge">{alerts.filter(a => a.type === 'success').length} Positive</span>
                            )}
                        </span>
                    </div>
                </div>
                {alerts.length > 3 && (
                    <button
                        className="expand-btn"
                        onClick={() => setExpanded(!expanded)}
                    >
                        {expanded ? 'Show Less' : `Show All (${alerts.length})`}
                    </button>
                )}
            </div>

            {/* Alert Cards */}
            <div className="risk-alerts-grid">
                {displayAlerts.map((alert, index) => (
                    <div
                        key={index}
                        className={`risk-alert-card ${getAlertClass(alert.type)}`}
                    >
                        <div className="alert-header">
                            <div className="alert-icon">
                                {getAlertIcon(alert.type)}
                            </div>
                            <div className="alert-title-section">
                                <span className="alert-emoji">{alert.icon}</span>
                                <span className="alert-title">{alert.title}</span>
                            </div>
                        </div>
                        <p className="alert-message">{alert.message}</p>
                        <div className="alert-action">
                            <span className="action-label">Action:</span>
                            <span className="action-text">{alert.action}</span>
                        </div>
                    </div>
                ))}
            </div>

            <style>{`
                .risk-alerts-container {
                    margin-bottom: var(--spacing-xl);
                }

                .risk-summary-banner {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: var(--spacing-md) var(--spacing-lg);
                    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
                    color: white;
                }

                .risk-summary-content {
                    display: flex;
                    align-items: center;
                    gap: var(--spacing-md);
                }

                .risk-icon {
                    color: #fbbf24;
                }

                .risk-summary-text {
                    display: flex;
                    flex-direction: column;
                    gap: 2px;
                }

                .risk-title {
                    font-weight: 600;
                    font-size: var(--font-size-base);
                }

                .risk-count {
                    display: flex;
                    gap: var(--spacing-sm);
                    font-size: var(--font-size-sm);
                }

                .critical-badge {
                    background: rgba(239, 68, 68, 0.9);
                    padding: 2px 8px;
                    border-radius: var(--radius-full);
                    font-size: var(--font-size-xs);
                }

                .warning-badge {
                    background: rgba(245, 158, 11, 0.9);
                    padding: 2px 8px;
                    border-radius: var(--radius-full);
                    font-size: var(--font-size-xs);
                }

                .success-badge {
                    background: rgba(16, 185, 129, 0.9);
                    padding: 2px 8px;
                    border-radius: var(--radius-full);
                    font-size: var(--font-size-xs);
                }

                .expand-btn {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    color: white;
                    padding: var(--spacing-xs) var(--spacing-md);
                    border-radius: var(--radius-md);
                    cursor: pointer;
                    font-size: var(--font-size-sm);
                    transition: all var(--transition-fast);
                }

                .expand-btn:hover {
                    background: rgba(255, 255, 255, 0.2);
                }

                .risk-alerts-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: var(--spacing-md);
                    padding: var(--spacing-lg);
                    background: var(--bg-card);
                    border: 1px solid var(--border);
                    border-top: none;
                    border-radius: 0 0 var(--radius-lg) var(--radius-lg);
                }

                .risk-alert-card {
                    padding: var(--spacing-md);
                    border-radius: var(--radius-md);
                    border-left: 4px solid;
                }

                .alert-critical {
                    background: rgba(239, 68, 68, 0.08);
                    border-color: #ef4444;
                }

                .alert-warning {
                    background: rgba(245, 158, 11, 0.08);
                    border-color: #f59e0b;
                }

                .alert-success {
                    background: rgba(16, 185, 129, 0.08);
                    border-color: #10b981;
                }

                .alert-info {
                    background: rgba(59, 130, 246, 0.08);
                    border-color: #3b82f6;
                }

                .alert-header {
                    display: flex;
                    align-items: center;
                    gap: var(--spacing-sm);
                    margin-bottom: var(--spacing-sm);
                }

                .alert-icon {
                    display: flex;
                }

                .alert-critical .alert-icon { color: #ef4444; }
                .alert-warning .alert-icon { color: #f59e0b; }
                .alert-success .alert-icon { color: #10b981; }
                .alert-info .alert-icon { color: #3b82f6; }

                .alert-title-section {
                    display: flex;
                    align-items: center;
                    gap: var(--spacing-xs);
                }

                .alert-emoji {
                    font-size: var(--font-size-lg);
                }

                .alert-title {
                    font-weight: 600;
                    font-size: var(--font-size-sm);
                    color: var(--text-primary);
                }

                .alert-message {
                    font-size: var(--font-size-sm);
                    color: var(--text-secondary);
                    margin-bottom: var(--spacing-sm);
                    line-height: 1.5;
                }

                .alert-action {
                    background: rgba(0, 0, 0, 0.03);
                    padding: var(--spacing-xs) var(--spacing-sm);
                    border-radius: var(--radius-sm);
                    font-size: var(--font-size-xs);
                }

                .action-label {
                    font-weight: 600;
                    color: var(--text-primary);
                    margin-right: var(--spacing-xs);
                }

                .action-text {
                    color: var(--text-secondary);
                }

                @media (max-width: 768px) {
                    .risk-alerts-grid {
                        grid-template-columns: 1fr;
                    }
                }
            `}</style>
        </div>
    );
}

export default RiskAlertsBanner;
