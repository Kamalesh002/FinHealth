import { useTranslation } from 'react-i18next';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

function HealthScoreCard({ score, grade, riskLevel, previousScore }) {
    const { t } = useTranslation();

    const getScoreColor = (score) => {
        if (score >= 75) return 'excellent';
        if (score >= 55) return 'good';
        if (score >= 35) return 'average';
        return 'poor';
    };

    const getGradeColor = (grade) => {
        if (grade?.startsWith('A')) return '#10b981';
        if (grade?.startsWith('B')) return '#22c55e';
        if (grade?.startsWith('C')) return '#f59e0b';
        return '#ef4444';
    };

    const getTrend = () => {
        if (!previousScore) return null;
        const diff = score - previousScore;
        if (diff > 2) return { icon: TrendingUp, color: '#10b981', text: `+${diff.toFixed(1)}` };
        if (diff < -2) return { icon: TrendingDown, color: '#ef4444', text: diff.toFixed(1) };
        return { icon: Minus, color: '#64748b', text: '0' };
    };

    const trend = getTrend();
    const scoreColor = getScoreColor(score);

    // Calculate stroke offset for circular progress
    const circumference = 2 * Math.PI * 54;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    return (
        <div className="health-score-card">
            <div className="score-header">
                <h3>{t('dashboard.healthScore')}</h3>
                {trend && (
                    <div className="score-trend" style={{ color: trend.color }}>
                        <trend.icon size={16} />
                        <span>{trend.text}</span>
                    </div>
                )}
            </div>

            <div className="score-visual">
                <svg className="score-ring" viewBox="0 0 120 120">
                    {/* Background circle */}
                    <circle
                        cx="60"
                        cy="60"
                        r="54"
                        fill="none"
                        stroke="var(--border)"
                        strokeWidth="8"
                    />
                    {/* Progress circle */}
                    <circle
                        cx="60"
                        cy="60"
                        r="54"
                        fill="none"
                        stroke={`url(#scoreGradient-${scoreColor})`}
                        strokeWidth="8"
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        strokeDashoffset={strokeDashoffset}
                        transform="rotate(-90 60 60)"
                        style={{ transition: 'stroke-dashoffset 1s ease-out' }}
                    />
                    {/* Gradient definitions */}
                    <defs>
                        <linearGradient id="scoreGradient-excellent" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#10b981" />
                            <stop offset="100%" stopColor="#34d399" />
                        </linearGradient>
                        <linearGradient id="scoreGradient-good" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#22c55e" />
                            <stop offset="100%" stopColor="#84cc16" />
                        </linearGradient>
                        <linearGradient id="scoreGradient-average" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#f59e0b" />
                            <stop offset="100%" stopColor="#fbbf24" />
                        </linearGradient>
                        <linearGradient id="scoreGradient-poor" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#ef4444" />
                            <stop offset="100%" stopColor="#f87171" />
                        </linearGradient>
                    </defs>
                </svg>

                <div className="score-value">
                    <span className="score-number">{Math.round(score)}</span>
                    <span className="score-max">/100</span>
                </div>
            </div>

            <div className="score-details">
                <div className="score-grade" style={{ backgroundColor: getGradeColor(grade) + '20', color: getGradeColor(grade) }}>
                    Grade: {grade}
                </div>
                <div className={`risk-pill ${riskLevel?.toLowerCase()}`}>
                    {t('dashboard.riskLevel')}: {t(`risk.${riskLevel}`)}
                </div>
            </div>

            <style>{`
        .health-score-card {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--spacing-lg);
          border: 1px solid var(--border);
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        .score-header {
          width: 100%;
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: var(--spacing-lg);
        }

        .score-header h3 {
          font-size: var(--font-size-lg);
          font-weight: 600;
          color: var(--text-primary);
        }

        .score-trend {
          display: flex;
          align-items: center;
          gap: var(--spacing-xs);
          font-size: var(--font-size-sm);
          font-weight: 600;
        }

        .score-visual {
          position: relative;
          width: 140px;
          height: 140px;
          margin-bottom: var(--spacing-lg);
        }

        .score-ring {
          width: 100%;
          height: 100%;
        }

        .score-value {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          text-align: center;
        }

        .score-number {
          font-size: var(--font-size-3xl);
          font-weight: 700;
          color: var(--text-primary);
        }

        .score-max {
          font-size: var(--font-size-sm);
          color: var(--text-muted);
        }

        .score-details {
          display: flex;
          gap: var(--spacing-md);
          flex-wrap: wrap;
          justify-content: center;
        }

        .score-grade {
          padding: var(--spacing-xs) var(--spacing-md);
          border-radius: var(--radius-full);
          font-size: var(--font-size-sm);
          font-weight: 600;
        }
      `}</style>
        </div>
    );
}

export default HealthScoreCard;
