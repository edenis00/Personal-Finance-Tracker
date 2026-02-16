// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import LoginPage from './components/Login/Page';
import RegisterPage from './components/Register/Page';
import Dashboard from './components/Dashboard/Dashboard';
import IncomePage from './components/Income/IncomePage';
import ExpensePage from './components/Expense/ExpensePage';
import SavingsPage from './components/Savings/SavingsPage';
import ProfilePage from './components/Profile/ProfilePage';
import AdminDashboard from './components/Admin/AdminDashboard';
import Layout from './components/Layout/Layout';
import Loader from './components/UI/Loader';
import api from './services/api';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const userData = await api.getCurrentUser();
        setUser(userData);
        setIsAuthenticated(true);
      } catch (error) {
        localStorage.removeItem('token');
        setIsAuthenticated(false);
      }
    }
    setLoading(false);
  };

  const handleLogin = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    api.clearToken();
    setUser(null);
    setIsAuthenticated(false);
  };

  if (loading) {
    return <Loader fullScreen />;
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route
          path="/login"
          element={
            !isAuthenticated ? (
              <LoginPage onLogin={handleLogin} />
            ) : (
              <Navigate to="/dashboard" replace />
            )
          }
        />
        <Route
          path="/register"
          element={
            !isAuthenticated ? (
              <RegisterPage />
            ) : (
              <Navigate to="/dashboard" replace />
            )
          }
        />

        {/* Protected Routes */}
        <Route
          path="/"
          element={
            isAuthenticated ? (
              <Layout user={user} onLogout={handleLogout} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="income" element={<IncomePage />} />
          <Route path="expenses" element={<ExpensePage />} />
          <Route path="savings" element={<SavingsPage />} />
          <Route path="profile" element={<ProfilePage />} />
          {user?.role === 'admin' && (
            <Route path="admin" element={<AdminDashboard />} />
          )}
        </Route>

        {/* Catch all */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;