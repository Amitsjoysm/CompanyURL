import React from 'react';
import { Link } from 'react-router-dom';
import { Search, Mail, Twitter, Linkedin, Github } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300" data-testid="footer">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Search className="w-8 h-8 text-emerald-500" />
              <span className="text-xl font-bold text-white">CorpInfo</span>
            </div>
            <p className="text-sm text-gray-400">
              Production-ready company data crawler. Find LinkedIn URLs, enrich company data, and power your business intelligence.
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className="font-semibold text-white mb-4">Product</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/" className="hover:text-emerald-500 transition" data-testid="footer-home">Home</Link></li>
              <li><Link to="/pricing" className="hover:text-emerald-500 transition" data-testid="footer-pricing">Pricing</Link></li>
              <li><Link to="/dashboard" className="hover:text-emerald-500 transition">Dashboard</Link></li>
              <li><a href="/docs" className="hover:text-emerald-500 transition">API Docs</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-semibold text-white mb-4">Resources</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/blogs" className="hover:text-emerald-500 transition" data-testid="footer-blog">Blog</Link></li>
              <li><Link to="/faq" className="hover:text-emerald-500 transition" data-testid="footer-faq">FAQ</Link></li>
              <li><a href="#" className="hover:text-emerald-500 transition">Support</a></li>
              <li><a href="#" className="hover:text-emerald-500 transition">Contact</a></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="font-semibold text-white mb-4">Legal</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-emerald-500 transition">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-emerald-500 transition">Terms of Service</a></li>
              <li><a href="#" className="hover:text-emerald-500 transition">GDPR</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col sm:flex-row justify-between items-center">
          <p className="text-sm text-gray-400">
            © 2025 CorpInfo. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 sm:mt-0">
            <a href="#" className="text-gray-400 hover:text-emerald-500 transition">
              <Twitter className="w-5 h-5" />
            </a>
            <a href="#" className="text-gray-400 hover:text-emerald-500 transition">
              <Linkedin className="w-5 h-5" />
            </a>
            <a href="#" className="text-gray-400 hover:text-emerald-500 transition">
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
