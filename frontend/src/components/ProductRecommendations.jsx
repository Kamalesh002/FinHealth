import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { analysisAPI } from '../services/api';
import './ProductRecommendations.css';

const ProductRecommendations = ({ companyId }) => {
    const { t } = useTranslation();
    const [recommendations, setRecommendations] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [expandedProduct, setExpandedProduct] = useState(null);

    useEffect(() => {
        if (companyId) {
            fetchRecommendations();
        }
    }, [companyId]);

    const fetchRecommendations = async () => {
        try {
            setLoading(true);
            const response = await analysisAPI.getProductRecommendations(companyId);
            setRecommendations(response.data);
            setError(null);
        } catch (err) {
            setError('Failed to load recommendations');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const getQualificationBadge = (status) => {
        const styles = {
            highly_likely: { bg: '#10B981', text: 'Highly Likely' },
            likely: { bg: '#3B82F6', text: 'Likely to Qualify' },
            possible: { bg: '#F59E0B', text: 'Possible' },
            needs_improvement: { bg: '#6B7280', text: 'Build Credit First' }
        };
        const style = styles[status] || styles.possible;
        return (
            <span className="qualification-badge" style={{ backgroundColor: style.bg }}>
                {style.text}
            </span>
        );
    };

    const getProductIcon = (type) => {
        const icons = {
            working_capital_loan: '💰',
            invoice_discounting: '📄',
            msme_credit_line: '🏦',
            overdraft_facility: '🔄',
            term_loan: '📈',
            equipment_financing: '🔧',
            government_scheme: '🏛️',
            trade_finance: '🌐'
        };
        return icons[type] || '💳';
    };

    const ProductCard = ({ product, matchReasons, qualificationStatus, fitScore, isHighlighted }) => (
        <div
            className={`product-card ${isHighlighted ? 'highlighted' : ''} ${expandedProduct === product.id ? 'expanded' : ''}`}
            onClick={() => setExpandedProduct(expandedProduct === product.id ? null : product.id)}
        >
            <div className="product-header">
                <div className="product-icon">{getProductIcon(product.type)}</div>
                <div className="product-title">
                    <h3>{product.name}</h3>
                    <span className="provider-type">{product.provider_type}</span>
                </div>
                {fitScore && (
                    <div className="fit-score">
                        <div className="score-circle" style={{
                            background: `conic-gradient(#10B981 ${fitScore}%, #1F2937 0)`
                        }}>
                            <span>{Math.round(fitScore)}%</span>
                        </div>
                        <span className="score-label">Match</span>
                    </div>
                )}
            </div>

            <p className="product-description">{product.description}</p>

            {qualificationStatus && getQualificationBadge(qualificationStatus)}

            {matchReasons && matchReasons.length > 0 && (
                <div className="match-reasons">
                    {matchReasons.map((reason, idx) => (
                        <span key={idx} className="reason-tag">✓ {reason}</span>
                    ))}
                </div>
            )}

            <div className="product-highlights">
                <div className="highlight">
                    <span className="label">Interest Rate</span>
                    <span className="value">{product.interest_rate_range}</span>
                </div>
                <div className="highlight">
                    <span className="label">Amount</span>
                    <span className="value">{product.loan_amount_range}</span>
                </div>
                <div className="highlight">
                    <span className="label">Tenure</span>
                    <span className="value">{product.tenure_range}</span>
                </div>
            </div>

            {expandedProduct === product.id && (
                <div className="product-details">
                    <div className="detail-section">
                        <h4>Ideal For</h4>
                        <div className="tags">
                            {product.ideal_for.map((item, idx) => (
                                <span key={idx} className="tag ideal">{item}</span>
                            ))}
                        </div>
                    </div>

                    <div className="detail-section">
                        <h4>Key Features</h4>
                        <ul>
                            {product.features.map((feature, idx) => (
                                <li key={idx}>✅ {feature}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="detail-section">
                        <h4>Eligibility Criteria</h4>
                        <ul>
                            {product.eligibility_criteria.map((criteria, idx) => (
                                <li key={idx}>• {criteria}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="detail-section">
                        <h4>Documents Required</h4>
                        <div className="tags">
                            {product.documents_required.map((doc, idx) => (
                                <span key={idx} className="tag doc">📎 {doc}</span>
                            ))}
                        </div>
                    </div>

                    <button className="apply-btn">
                        Apply Now →
                    </button>
                </div>
            )}

            <div className="expand-hint">
                {expandedProduct === product.id ? 'Click to collapse' : 'Click for details'}
            </div>
        </div>
    );

    if (loading) {
        return (
            <div className="recommendations-loading">
                <div className="loader"></div>
                <p>Analyzing your profile for best financing options...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="recommendations-error">
                <span>⚠️</span>
                <p>{error}</p>
                <button onClick={fetchRecommendations}>Retry</button>
            </div>
        );
    }

    if (!recommendations) return null;

    return (
        <div className="product-recommendations">
            <div className="recommendations-header">
                <div className="header-content">
                    <h2>💳 Financing Options for Your Business</h2>
                    <p>Based on your financial health score of <strong>{recommendations.health_score}</strong></p>
                </div>
            </div>

            {recommendations.summary && (
                <div className="summary-card">
                    <div className="summary-icon">💡</div>
                    <p>{recommendations.summary}</p>
                </div>
            )}

            {recommendations.highly_recommended && recommendations.highly_recommended.length > 0 && (
                <section className="recommendation-section">
                    <h3 className="section-title">
                        <span className="icon">🎯</span>
                        Highly Recommended for You
                    </h3>
                    <div className="products-grid">
                        {recommendations.highly_recommended.map((item, idx) => (
                            <ProductCard
                                key={idx}
                                product={item.product}
                                matchReasons={item.match_reasons}
                                qualificationStatus={item.qualification_status}
                                fitScore={item.fit_score}
                                isHighlighted={true}
                            />
                        ))}
                    </div>
                </section>
            )}

            {recommendations.good_options && recommendations.good_options.length > 0 && (
                <section className="recommendation-section">
                    <h3 className="section-title">
                        <span className="icon">👍</span>
                        Good Options to Consider
                    </h3>
                    <div className="products-grid">
                        {recommendations.good_options.map((item, idx) => (
                            <ProductCard
                                key={idx}
                                product={item.product}
                                matchReasons={item.match_reasons}
                                qualificationStatus={item.qualification_status}
                                fitScore={item.fit_score}
                                isHighlighted={false}
                            />
                        ))}
                    </div>
                </section>
            )}

            {recommendations.consider_later && recommendations.consider_later.length > 0 && (
                <section className="recommendation-section">
                    <h3 className="section-title">
                        <span className="icon">📋</span>
                        Consider Later
                    </h3>
                    <div className="products-grid compact">
                        {recommendations.consider_later.map((item, idx) => (
                            <ProductCard
                                key={idx}
                                product={item.product}
                                matchReasons={item.match_reasons}
                                qualificationStatus={item.qualification_status}
                                fitScore={item.fit_score}
                                isHighlighted={false}
                            />
                        ))}
                    </div>
                </section>
            )}

            {recommendations.next_steps && recommendations.next_steps.length > 0 && (
                <div className="next-steps-card">
                    <h3>📝 Next Steps</h3>
                    <ol>
                        {recommendations.next_steps.map((step, idx) => (
                            <li key={idx}>{step}</li>
                        ))}
                    </ol>
                </div>
            )}
        </div>
    );
};

export default ProductRecommendations;
