import { useState, useEffect, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { AuthContext } from '../App';
import { companyAPI, analysisAPI } from '../services/api';
import HealthScoreCard from '../components/HealthScoreCard';
import ChatInterface from '../components/ChatInterface';
import RiskAlertsBanner from '../components/RiskAlertsBanner';
import CFOInsights from '../components/CFOInsights';
import ActionPlanButton from '../components/ActionPlanButton';
import {
    Building2, Plus, ArrowRight, TrendingUp, Calendar,
    AlertTriangle, Wallet, Factory, ShoppingBag, Tractor,
    Briefcase, Truck, ShoppingCart
} from 'lucide-react';

const industryIcons = {
    Manufacturing: Factory,
    Retail: ShoppingBag,
    Agriculture: Tractor,
    Services: Briefcase,
    Logistics: Truck,
    'E-commerce': ShoppingCart
};

function Dashboard() {
    const { user } = useContext(AuthContext);
    const { t } = useTranslation();
    const navigate = useNavigate();

    const [companies, setCompanies] = useState([]);
    const [selectedCompany, setSelectedCompany] = useState(null);
    const [healthScore, setHealthScore] = useState(null);
    const [loading, setLoading] = useState(true);
    const [showNewCompany, setShowNewCompany] = useState(false);
    const [newCompany, setNewCompany] = useState({ name: '', industry: 'Services' });

    useEffect(() => {
        loadCompanies();
    }, []);

    useEffect(() => {
        if (selectedCompany) {
            loadHealthScore(selectedCompany.id);
        }
    }, [selectedCompany]);

    const loadCompanies = async () => {
        try {
            const response = await companyAPI.getAll();
            setCompanies(response.data);
            if (response.data.length > 0) {
                setSelectedCompany(response.data[0]);
            }
        } catch (error) {
            console.error('Failed to load companies:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadHealthScore = async (companyId) => {
        try {
            const response = await analysisAPI.getHealthScore(companyId);
            setHealthScore(response.data);
        } catch (error) {
            setHealthScore(null);
        }
    };

    const handleCreateCompany = async (e) => {
        e.preventDefault();
        try {
            const response = await companyAPI.create(newCompany);
            setCompanies([...companies, response.data]);
            setSelectedCompany(response.data);
            setShowNewCompany(false);
            setNewCompany({ name: '', industry: 'Services' });
        } catch (error) {
            console.error('Failed to create company:', error);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center" style={{ height: '60vh' }}>
                <div className="loader"></div>
            </div>
        );
    }

    return (
        <div className="dashboard">
            {/* Header */}
            <div className="dashboard-header">
                <div>
                    <h1>{t('dashboard.title')}</h1>
                    <p className="text-secondary">{t('dashboard.welcome')}, {user?.full_name}!</p>
                </div>
                <button className="btn btn-primary" onClick={() => setShowNewCompany(true)}>
                    <Plus size={18} />
                    <span>{t('dashboard.addCompany')}</span>
                </button>
            </div>

            {/* Company Selector */}
            {companies.length > 0 && (
                <div className="company-tabs">
                    {companies.map((company) => {
                        const Icon = industryIcons[company.industry] || Building2;
                        return (
                            <button
                                key={company.id}
                                className={`company-tab ${selectedCompany?.id === company.id ? 'active' : ''}`}
                                onClick={() => setSelectedCompany(company)}
                            >
                                <Icon size={18} />
                                <span>{company.name}</span>
                            </button>
                        );
                    })}
                </div>
            )}

            {/* Main Content */}
            {selectedCompany ? (
                <div className="dashboard-grid">
                    {/* Left Column */}
                    <div className="dashboard-main">
                        {healthScore ? (
                            <>
                                {/* 🚨 Smart Risk Alerts - NEW! */}
                                <RiskAlertsBanner companyId={selectedCompany.id} />

                                {/* Health Score */}
                                <HealthScoreCard
                                    score={healthScore.overall_score}
                                    grade={healthScore.score_grade}
                                    riskLevel={healthScore.risk_level}
                                />

                                {/* 💡 CFO Insights - NEW! */}
                                <CFOInsights companyId={selectedCompany.id} />

                                {/* Quick Stats */}
                                <div className="quick-stats">
                                    <div className="stat-card">
                                        <div className="stat-icon cash">
                                            <Wallet size={20} />
                                        </div>
                                        <div className="stat-content">
                                            <span className="stat-label">{t('dashboard.cashRunway')}</span>
                                            <span className="stat-value">
                                                {healthScore.metrics?.cash_runway_days || 0} {t('dashboard.days')}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="stat-card">
                                        <div className="stat-icon profit">
                                            <TrendingUp size={20} />
                                        </div>
                                        <div className="stat-content">
                                            <span className="stat-label">Net Margin</span>
                                            <span className="stat-value">
                                                {healthScore.metrics?.net_margin?.toFixed(1) || 0}%
                                            </span>
                                        </div>
                                    </div>
                                    <div className="stat-card">
                                        <div className="stat-icon risk">
                                            <AlertTriangle size={20} />
                                        </div>
                                        <div className="stat-content">
                                            <span className="stat-label">Risk Factors</span>
                                            <span className="stat-value">
                                                {healthScore.risk_factors?.length || 0}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="stat-card">
                                        <div className="stat-icon calendar">
                                            <Calendar size={20} />
                                        </div>
                                        <div className="stat-content">
                                            <span className="stat-label">WC Cycle</span>
                                            <span className="stat-value">
                                                {healthScore.metrics?.working_capital_cycle || 0} days
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                {/* Action Buttons */}
                                <div className="action-buttons-grid">
                                    {/* 📋 90-Day Action Plan - NEW! */}
                                    <ActionPlanButton
                                        companyId={selectedCompany.id}
                                        companyName={selectedCompany.name}
                                    />

                                    {/* View Analysis Button */}
                                    <Link to={`/analysis/${selectedCompany.id}`} className="btn btn-secondary btn-lg full-width">
                                        <span>{t('dashboard.viewAnalysis')}</span>
                                        <ArrowRight size={18} />
                                    </Link>
                                </div>
                            </>
                        ) : (
                            <div className="no-data-card">
                                <TrendingUp size={48} className="no-data-icon" />
                                <h3>No Financial Data Yet</h3>
                                <p>Upload and validate your financial documents to see your health score.</p>
                                <Link to="/upload" className="btn btn-primary">
                                    Upload Documents
                                </Link>
                            </div>
                        )}
                    </div>

                    {/* Right Column - Chat */}
                    <div className="dashboard-sidebar">
                        <ChatInterface companyId={selectedCompany.id} />
                    </div>
                </div>
            ) : (
                <div className="no-companies">
                    <Building2 size={64} className="no-data-icon" />
                    <h2>{t('dashboard.noCompanies')}</h2>
                    <p>Get started by adding your first company</p>
                    <button className="btn btn-primary btn-lg" onClick={() => setShowNewCompany(true)}>
                        <Plus size={18} />
                        <span>{t('dashboard.addCompany')}</span>
                    </button>
                </div>
            )}

            {/* New Company Modal */}
            {showNewCompany && (
                <div className="modal-overlay" onClick={() => setShowNewCompany(false)}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <h2>{t('upload.newCompany')}</h2>
                        <form onSubmit={handleCreateCompany}>
                            <div className="form-group">
                                <label className="form-label">Company Name</label>
                                <input
                                    type="text"
                                    className="form-input"
                                    value={newCompany.name}
                                    onChange={(e) => setNewCompany({ ...newCompany, name: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">Industry</label>
                                <select
                                    className="form-select"
                                    value={newCompany.industry}
                                    onChange={(e) => setNewCompany({ ...newCompany, industry: e.target.value })}
                                >
                                    {['Manufacturing', 'Retail', 'Agriculture', 'Services', 'Logistics', 'E-commerce'].map((ind) => (
                                        <option key={ind} value={ind}>{t(`industries.${ind}`)}</option>
                                    ))}
                                </select>
                            </div>
                            <div className="modal-actions">
                                <button type="button" className="btn btn-secondary" onClick={() => setShowNewCompany(false)}>
                                    {t('common.cancel')}
                                </button>
                                <button type="submit" className="btn btn-primary">
                                    Create Company
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <style>{`
        .dashboard-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: var(--spacing-xl);
        }

        .dashboard-header h1 {
          font-size: var(--font-size-2xl);
          font-weight: 700;
        }

        .company-tabs {
          display: flex;
          gap: var(--spacing-sm);
          margin-bottom: var(--spacing-xl);
          overflow-x: auto;
          padding-bottom: var(--spacing-sm);
        }

        .company-tab {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          padding: var(--spacing-sm) var(--spacing-lg);
          background: var(--bg-card);
          border: 1px solid var(--border);
          border-radius: var(--radius-full);
          color: var(--text-secondary);
          cursor: pointer;
          transition: all var(--transition-fast);
          white-space: nowrap;
        }

        .company-tab:hover {
          border-color: var(--primary);
          color: var(--text-primary);
        }

        .company-tab.active {
          background: var(--gradient-primary);
          border-color: transparent;
          color: white;
        }

        .dashboard-grid {
          display: grid;
          grid-template-columns: 1fr 400px;
          gap: var(--spacing-xl);
        }

        .dashboard-main {
          display: flex;
          flex-direction: column;
          gap: var(--spacing-lg);
        }

        .quick-stats {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: var(--spacing-md);
        }

        .stat-card {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--spacing-md);
          border: 1px solid var(--border);
          display: flex;
          align-items: center;
          gap: var(--spacing-md);
        }

        .stat-icon {
          width: 44px;
          height: 44px;
          border-radius: var(--radius-md);
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .stat-icon.cash { background: rgba(16, 185, 129, 0.2); color: var(--success); }
        .stat-icon.profit { background: rgba(99, 102, 241, 0.2); color: var(--primary); }
        .stat-icon.risk { background: rgba(245, 158, 11, 0.2); color: var(--warning); }
        .stat-icon.calendar { background: rgba(14, 165, 233, 0.2); color: var(--secondary); }

        .stat-content {
          display: flex;
          flex-direction: column;
        }

        .stat-label {
          font-size: var(--font-size-xs);
          color: var(--text-muted);
        }

        .stat-value {
          font-size: var(--font-size-lg);
          font-weight: 600;
        }

        .full-width {
          width: 100%;
          justify-content: center;
        }

        .action-buttons-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: var(--spacing-md);
        }

        @media (max-width: 768px) {
          .action-buttons-grid {
            grid-template-columns: 1fr;
          }
        }

        .no-data-card, .no-companies {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--spacing-2xl);
          border: 1px solid var(--border);
          text-align: center;
        }

        .no-data-icon {
          color: var(--text-muted);
          margin-bottom: var(--spacing-md);
        }

        .no-data-card h3, .no-companies h2 {
          margin-bottom: var(--spacing-sm);
        }

        .no-data-card p, .no-companies p {
          color: var(--text-secondary);
          margin-bottom: var(--spacing-lg);
        }

        .modal-overlay {
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
        }

        .modal {
          background: var(--bg-card);
          border-radius: var(--radius-xl);
          padding: var(--spacing-xl);
          width: 100%;
          max-width: 400px;
          border: 1px solid var(--border);
        }

        .modal h2 {
          margin-bottom: var(--spacing-lg);
        }

        .modal-actions {
          display: flex;
          gap: var(--spacing-md);
          margin-top: var(--spacing-lg);
        }

        .modal-actions .btn {
          flex: 1;
        }

        @media (max-width: 1024px) {
          .dashboard-grid {
            grid-template-columns: 1fr;
          }
          .quick-stats {
            grid-template-columns: repeat(2, 1fr);
          }
        }

        @media (max-width: 640px) {
          .quick-stats {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
        </div>
    );
}

export default Dashboard;
