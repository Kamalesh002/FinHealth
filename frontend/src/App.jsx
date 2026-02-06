import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect, createContext } from 'react';
import { useTranslation } from 'react-i18next';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import Analysis from './pages/Analysis';
import Login from './pages/Login';
import Register from './pages/Register';

// Auth Context
export const AuthContext = createContext(null);

function App() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const { i18n } = useTranslation();

    useEffect(() => {
        // Check for existing token
        const token = localStorage.getItem('token');
        const userData = localStorage.getItem('user');
        if (token && userData) {
            setUser(JSON.parse(userData));
        }
        setLoading(false);
    }, []);

    const login = (userData, token) => {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
        if (userData.preferred_language) {
            i18n.changeLanguage(userData.preferred_language);
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
    };

    if (loading) {
        return (
            <div className="app-container flex items-center justify-center">
                <div className="loader"></div>
            </div>
        );
    }

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            <BrowserRouter>
                <div className="app-container">
                    {user && <Navbar />}
                    <main className="main-content">
                        <Routes>
                            {/* Public Routes */}
                            <Route
                                path="/login"
                                element={user ? <Navigate to="/dashboard" /> : <Login />}
                            />
                            <Route
                                path="/register"
                                element={user ? <Navigate to="/dashboard" /> : <Register />}
                            />

                            {/* Protected Routes */}
                            <Route
                                path="/dashboard"
                                element={user ? <Dashboard /> : <Navigate to="/login" />}
                            />
                            <Route
                                path="/upload"
                                element={user ? <Upload /> : <Navigate to="/login" />}
                            />
                            <Route
                                path="/analysis/:companyId?"
                                element={user ? <Analysis /> : <Navigate to="/login" />}
                            />

                            {/* Default */}
                            <Route path="/" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
                            <Route path="*" element={<Navigate to="/" />} />
                        </Routes>
                    </main>
                </div>
            </BrowserRouter>
        </AuthContext.Provider>
    );
}

export default App;
