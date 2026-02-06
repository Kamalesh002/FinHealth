import { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../App';
import { authAPI } from '../services/api';
import { TrendingUp, Mail, Lock, User, Globe, AlertCircle } from 'lucide-react';

function Register() {
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        full_name: '',
        preferred_language: 'en'
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            // Register
            await authAPI.register(formData);
            // Auto login
            const loginResponse = await authAPI.login({
                email: formData.email,
                password: formData.password
            });
            login(loginResponse.data.user, loginResponse.data.access_token);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-card animate-fadeIn">
                {/* Header */}
                <div className="auth-header">
                    <div className="logo-icon">
                        <TrendingUp size={32} />
                    </div>
                    <h1>Create Account</h1>
                    <p>Start your financial health journey today</p>
                </div>

                {/* Error */}
                {error && (
                    <div className="auth-error">
                        <AlertCircle size={16} />
                        <span>{error}</span>
                    </div>
                )}

                {/* Form */}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Full Name</label>
                        <div className="input-with-icon">
                            <User size={18} className="input-icon" />
                            <input
                                type="text"
                                className="form-input"
                                placeholder="John Doe"
                                value={formData.full_name}
                                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Email</label>
                        <div className="input-with-icon">
                            <Mail size={18} className="input-icon" />
                            <input
                                type="email"
                                className="form-input"
                                placeholder="you@example.com"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <div className="input-with-icon">
                            <Lock size={18} className="input-icon" />
                            <input
                                type="password"
                                className="form-input"
                                placeholder="••••••••"
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                required
                                minLength={6}
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Preferred Language</label>
                        <div className="input-with-icon">
                            <Globe size={18} className="input-icon" />
                            <select
                                className="form-select"
                                value={formData.preferred_language}
                                onChange={(e) => setFormData({ ...formData, preferred_language: e.target.value })}
                                style={{ paddingLeft: '44px' }}
                            >
                                <option value="en">English</option>
                                <option value="hi">हिंदी (Hindi)</option>
                            </select>
                        </div>
                    </div>

                    <button type="submit" className="btn btn-primary btn-lg full-width" disabled={loading}>
                        {loading ? 'Creating Account...' : 'Create Account'}
                    </button>
                </form>

                {/* Footer */}
                <div className="auth-footer">
                    <p>Already have an account? <Link to="/login">Sign in</Link></p>
                </div>
            </div>

            <style>{`
        .auth-page {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: var(--spacing-lg);
        }

        .auth-card {
          width: 100%;
          max-width: 420px;
          background: var(--bg-card);
          border-radius: var(--radius-xl);
          padding: var(--spacing-2xl);
          border: 1px solid var(--border);
        }

        .auth-header {
          text-align: center;
          margin-bottom: var(--spacing-xl);
        }

        .auth-header .logo-icon {
          width: 64px;
          height: 64px;
          background: var(--gradient-primary);
          border-radius: var(--radius-lg);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          margin: 0 auto var(--spacing-md);
        }

        .auth-header h1 {
          font-size: var(--font-size-2xl);
          font-weight: 700;
          margin-bottom: var(--spacing-xs);
        }

        .auth-header p {
          color: var(--text-secondary);
          font-size: var(--font-size-sm);
        }

        .auth-error {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          padding: var(--spacing-sm) var(--spacing-md);
          background: rgba(239, 68, 68, 0.1);
          border: 1px solid rgba(239, 68, 68, 0.3);
          border-radius: var(--radius-md);
          color: var(--danger);
          font-size: var(--font-size-sm);
          margin-bottom: var(--spacing-lg);
        }

        .input-with-icon {
          position: relative;
        }

        .input-icon {
          position: absolute;
          left: var(--spacing-md);
          top: 50%;
          transform: translateY(-50%);
          color: var(--text-muted);
          z-index: 1;
        }

        .input-with-icon .form-input,
        .input-with-icon .form-select {
          padding-left: 44px;
        }

        .full-width {
          width: 100%;
        }

        .auth-footer {
          text-align: center;
          margin-top: var(--spacing-lg);
          font-size: var(--font-size-sm);
          color: var(--text-secondary);
        }

        .auth-footer a {
          color: var(--primary);
          text-decoration: none;
          font-weight: 500;
        }

        .auth-footer a:hover {
          text-decoration: underline;
        }
      `}</style>
        </div>
    );
}

export default Register;
