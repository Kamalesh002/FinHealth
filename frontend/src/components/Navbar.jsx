import { useContext } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { AuthContext } from '../App';
import { LayoutDashboard, Upload, BarChart3, LogOut, Globe, TrendingUp } from 'lucide-react';

function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const { t, i18n } = useTranslation();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'hi' : 'en';
    i18n.changeLanguage(newLang);
  };

  const navItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: t('nav.dashboard') },
    { path: '/upload', icon: Upload, label: t('nav.upload') },
    { path: '/analysis', icon: BarChart3, label: t('nav.analysis') }
  ];

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo */}
        <Link to="/dashboard" className="navbar-logo">
          <div className="logo-icon">
            <TrendingUp size={24} />
          </div>
          <span className="logo-text">FinHealth</span>
        </Link>

        {/* Navigation Links */}
        <div className="navbar-links">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
            >
              <item.icon size={18} />
              <span>{item.label}</span>
            </Link>
          ))}
        </div>

        {/* Right Section */}
        <div className="navbar-right">
          {/* Language Toggle */}
          <button onClick={toggleLanguage} className="lang-toggle" title="Toggle Language">
            <Globe size={18} />
            <span>{i18n.language.toUpperCase()}</span>
          </button>

          {/* User Info */}
          <div className="user-info">
            <span className="user-name">{user?.full_name || 'User'}</span>
          </div>

          {/* Logout */}
          <button onClick={handleLogout} className="btn btn-secondary logout-btn">
            <LogOut size={16} />
            <span>{t('nav.logout')}</span>
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
