import { useState } from 'react';
import { analysisAPI } from '../services/api';
import { FileText, Calendar, Target, Rocket, Hammer, TrendingUp, Download, Loader } from 'lucide-react';

function ActionPlanButton({ companyId, companyName }) {
    const [showModal, setShowModal] = useState(false);
    const [loading, setLoading] = useState(false);
    const [plan, setPlan] = useState(null);

    const generatePlan = async () => {
        setLoading(true);
        setShowModal(true);
        try {
            const response = await analysisAPI.getActionPlan(companyId);
            if (response.data.has_data) {
                setPlan(response.data.plan);
            }
        } catch (error) {
            console.error('Failed to generate action plan:', error);
        } finally {
            setLoading(false);
        }
    };

    const getPhaseIcon = (phase) => {
        switch (phase) {
            case 'Immediate Actions':
                return <Rocket size={20} />;
            case 'Structural Improvements':
                return <Hammer size={20} />;
            case 'Growth Actions':
                return <TrendingUp size={20} />;
            default:
                return <Target size={20} />;
        }
    };

    const downloadPlan = () => {
        if (!plan) return;

        const content = plan.plan_content || '';
        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${companyName || 'Company'}_90_Day_Action_Plan.md`;
        a.click();
        URL.revokeObjectURL(url);
    };

    return (
        <>
            <button
                className="action-plan-btn btn btn-primary btn-lg"
                onClick={generatePlan}
            >
                <FileText size={20} />
                <span>Generate 90-Day Action Plan</span>
            </button>

            {showModal && (
                <div className="action-plan-modal-overlay" onClick={() => setShowModal(false)}>
                    <div className="action-plan-modal" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <div className="modal-title-section">
                                <FileText size={24} />
                                <div>
                                    <h2>90-Day Financial Action Plan</h2>
                                    <p>{companyName}</p>
                                </div>
                            </div>
                            <button className="close-btn" onClick={() => setShowModal(false)}>×</button>
                        </div>

                        {loading ? (
                            <div className="loading-state">
                                <Loader size={40} className="spin" />
                                <p>Generating your personalized action plan...</p>
                                <span>This may take a few seconds</span>
                            </div>
                        ) : plan ? (
                            <div className="plan-content">
                                {/* Summary */}
                                <div className="plan-summary">
                                    <div className="summary-score">
                                        <span className="score-label">Health Score</span>
                                        <span className="score-value">{plan.health_score}/100</span>
                                    </div>
                                    <p className="summary-text">{plan.summary}</p>
                                </div>

                                {/* Phase Cards */}
                                <div className="phases-grid">
                                    {plan.phases?.map((phase, index) => (
                                        <div key={index} className="phase-card">
                                            <div className="phase-icon">
                                                {getPhaseIcon(phase.name)}
                                            </div>
                                            <div className="phase-info">
                                                <span className="phase-name">{phase.name}</span>
                                                <span className="phase-days">
                                                    <Calendar size={14} />
                                                    Days {phase.days}
                                                </span>
                                            </div>
                                            <span className="phase-focus">{phase.focus}</span>
                                        </div>
                                    ))}
                                </div>

                                {/* Plan Details */}
                                <div className="plan-details">
                                    <h3>Detailed Action Plan</h3>
                                    <div className="plan-text">
                                        {plan.plan_content?.split('\n').map((line, i) => {
                                            if (line.startsWith('# ')) {
                                                return <h2 key={i}>{line.replace('# ', '')}</h2>;
                                            } else if (line.startsWith('## ')) {
                                                return <h3 key={i}>{line.replace('## ', '')}</h3>;
                                            } else if (line.startsWith('### ')) {
                                                return <h4 key={i}>{line.replace('### ', '')}</h4>;
                                            } else if (line.startsWith('- ')) {
                                                return <li key={i}>{line.replace('- ', '')}</li>;
                                            } else if (line.startsWith('**') && line.endsWith('**')) {
                                                return <p key={i} className="bold">{line.replace(/\*\*/g, '')}</p>;
                                            } else if (line.trim()) {
                                                return <p key={i}>{line}</p>;
                                            }
                                            return null;
                                        })}
                                    </div>
                                </div>

                                {/* Actions */}
                                <div className="modal-actions">
                                    <button className="btn btn-secondary" onClick={() => setShowModal(false)}>
                                        Close
                                    </button>
                                    <button className="btn btn-primary" onClick={downloadPlan}>
                                        <Download size={18} />
                                        Download Plan
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <div className="error-state">
                                <p>Unable to generate action plan. Please try again.</p>
                                <button className="btn btn-primary" onClick={generatePlan}>
                                    Retry
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            )}

            <style>{`
                .action-plan-btn {
                    width: 100%;
                    gap: var(--spacing-sm);
                }

                .action-plan-modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0, 0, 0, 0.7);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1000;
                    padding: var(--spacing-lg);
                }

                .action-plan-modal {
                    background: var(--bg-card);
                    border-radius: var(--radius-xl);
                    width: 100%;
                    max-width: 800px;
                    max-height: 90vh;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                }

                .modal-header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: var(--spacing-lg);
                    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
                    color: white;
                }

                .modal-title-section {
                    display: flex;
                    align-items: center;
                    gap: var(--spacing-md);
                }

                .modal-title-section h2 {
                    margin: 0;
                    font-size: var(--font-size-xl);
                }

                .modal-title-section p {
                    margin: 0;
                    opacity: 0.9;
                    font-size: var(--font-size-sm);
                }

                .close-btn {
                    background: rgba(255, 255, 255, 0.2);
                    border: none;
                    color: white;
                    width: 36px;
                    height: 36px;
                    border-radius: var(--radius-full);
                    font-size: 24px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .close-btn:hover {
                    background: rgba(255, 255, 255, 0.3);
                }

                .loading-state, .error-state {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: var(--spacing-2xl);
                    text-align: center;
                    gap: var(--spacing-md);
                }

                .spin {
                    animation: spin 1s linear infinite;
                }

                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }

                .loading-state p {
                    font-size: var(--font-size-lg);
                    font-weight: 500;
                    color: var(--text-primary);
                    margin: 0;
                }

                .loading-state span {
                    font-size: var(--font-size-sm);
                    color: var(--text-muted);
                }

                .plan-content {
                    overflow-y: auto;
                    padding: var(--spacing-lg);
                }

                .plan-summary {
                    display: flex;
                    align-items: center;
                    gap: var(--spacing-lg);
                    padding: var(--spacing-lg);
                    background: var(--bg-secondary);
                    border-radius: var(--radius-lg);
                    margin-bottom: var(--spacing-lg);
                }

                .summary-score {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: var(--spacing-md);
                    background: var(--gradient-primary);
                    border-radius: var(--radius-lg);
                    color: white;
                    min-width: 100px;
                }

                .score-label {
                    font-size: var(--font-size-xs);
                    opacity: 0.9;
                }

                .score-value {
                    font-size: var(--font-size-2xl);
                    font-weight: 700;
                }

                .summary-text {
                    flex: 1;
                    color: var(--text-secondary);
                    line-height: 1.6;
                    margin: 0;
                }

                .phases-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: var(--spacing-md);
                    margin-bottom: var(--spacing-lg);
                }

                .phase-card {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                    padding: var(--spacing-md);
                    background: var(--bg-secondary);
                    border-radius: var(--radius-lg);
                    gap: var(--spacing-xs);
                }

                .phase-icon {
                    width: 48px;
                    height: 48px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: var(--gradient-primary);
                    color: white;
                    border-radius: var(--radius-full);
                }

                .phase-info {
                    display: flex;
                    flex-direction: column;
                    gap: 2px;
                }

                .phase-name {
                    font-weight: 600;
                    font-size: var(--font-size-sm);
                    color: var(--text-primary);
                }

                .phase-days {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 4px;
                    font-size: var(--font-size-xs);
                    color: var(--text-muted);
                }

                .phase-focus {
                    font-size: var(--font-size-xs);
                    color: var(--text-secondary);
                }

                .plan-details {
                    background: var(--bg-secondary);
                    border-radius: var(--radius-lg);
                    padding: var(--spacing-lg);
                    margin-bottom: var(--spacing-lg);
                }

                .plan-details h3 {
                    margin: 0 0 var(--spacing-md) 0;
                    font-size: var(--font-size-lg);
                    color: var(--text-primary);
                }

                .plan-text {
                    max-height: 300px;
                    overflow-y: auto;
                    font-size: var(--font-size-sm);
                    line-height: 1.7;
                    color: var(--text-secondary);
                }

                .plan-text h2 {
                    font-size: var(--font-size-lg);
                    color: var(--text-primary);
                    margin: var(--spacing-lg) 0 var(--spacing-sm) 0;
                }

                .plan-text h3 {
                    font-size: var(--font-size-base);
                    color: var(--text-primary);
                    margin: var(--spacing-md) 0 var(--spacing-sm) 0;
                }

                .plan-text h4 {
                    font-size: var(--font-size-sm);
                    color: var(--text-primary);
                    margin: var(--spacing-sm) 0;
                }

                .plan-text li {
                    margin-left: var(--spacing-lg);
                    margin-bottom: var(--spacing-xs);
                }

                .plan-text .bold {
                    font-weight: 600;
                    color: var(--text-primary);
                }

                .modal-actions {
                    display: flex;
                    gap: var(--spacing-md);
                    justify-content: flex-end;
                    padding-top: var(--spacing-lg);
                    border-top: 1px solid var(--border);
                }

                @media (max-width: 768px) {
                    .phases-grid {
                        grid-template-columns: 1fr;
                    }

                    .plan-summary {
                        flex-direction: column;
                    }
                }
            `}</style>
        </>
    );
}

export default ActionPlanButton;
