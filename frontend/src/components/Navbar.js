import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/button';
import { Search, LogOut, User, Shield } from 'lucide-react';

const Navbar = () => {
  const { user, logout, isAuthenticated, isSuperadmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2" data-testid="nav-logo">
            <Search className="w-8 h-8 text-emerald-600" />
            <span className="text-2xl font-bold bg-gradient-to-r from-emerald-600 to-emerald-500 bg-clip-text text-transparent">
              CorpInfo
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-emerald-600 transition font-medium" data-testid="nav-home">
              Home
            </Link>
            <Link to="/pricing" className="text-gray-700 hover:text-emerald-600 transition font-medium" data-testid="nav-pricing">
              Pricing
            </Link>
            <Link to="/blogs" className="text-gray-700 hover:text-emerald-600 transition font-medium" data-testid="nav-blogs">
              Blog
            </Link>
            <Link to="/faq" className="text-gray-700 hover:text-emerald-600 transition font-medium" data-testid="nav-faq">
              FAQ
            </Link>
            {isAuthenticated && (
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-emerald-600 transition font-medium" data-testid="nav-dashboard">
                  Dashboard
                </Link>
                <Link to="/api-tokens" className="text-gray-700 hover:text-emerald-600 transition font-medium" data-testid="nav-api-tokens">
                  API
                </Link>
              </>
            )}
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <div className="flex items-center space-x-3" data-testid="user-info">
                  <div className="text-right hidden sm:block">
                    <p className="text-sm font-medium text-gray-700">{user?.email}</p>
                    <p className="text-xs text-gray-500">{user?.credits || 0} credits</p>
                  </div>
                  {isSuperadmin && (
                    <Link to="/admin" data-testid="admin-link">
                      <Button variant="outline" size="sm" className="gap-2">
                        <Shield className="w-4 h-4" />
                        Admin
                      </Button>
                    </Link>
                  )}
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={handleLogout}
                    className="gap-2"
                    data-testid="logout-button"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </Button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" data-testid="login-link">
                  <Button variant="ghost" size="sm">Login</Button>
                </Link>
                <Link to="/register" data-testid="register-link">
                  <Button size="sm" className="bg-emerald-600 hover:bg-emerald-700">Sign Up</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
