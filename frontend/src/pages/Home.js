import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Search, Zap, Shield, TrendingUp, Check, ArrowRight } from 'lucide-react';
import { toast } from 'sonner';
import { crawl } from '../utils/api';

const Home = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [inputType, setInputType] = useState('domain');
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim()) {
      toast.error('Please enter a value to search');
      return;
    }

    if (!isAuthenticated) {
      toast.error('Please login to use the crawler');
      navigate('/login');
      return;
    }

    try {
      setLoading(true);
      const response = await crawl.single({ input_type: inputType, input_value: inputValue });
      toast.success('Crawl request created! Redirecting to dashboard...');
      setTimeout(() => navigate('/dashboard'), 1500);
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Failed to create crawl request';
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient py-20 px-4">
        <div className="max-w-5xl mx-auto text-center slide-up">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight" data-testid="hero-title">
            Find Company LinkedIn URLs
            <br />
            <span className="bg-gradient-to-r from-emerald-600 to-emerald-500 bg-clip-text text-transparent">
              In Seconds
            </span>
          </h1>
          <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto" data-testid="hero-description">
            Convert company domains to LinkedIn URLs. Enrich with industry, size, founders, and latest news. Built for sales teams, recruiters, and researchers.
          </p>

          {/* Search Form */}
          <div className="bg-white rounded-2xl shadow-xl p-8 max-w-3xl mx-auto fade-in">
            <form onSubmit={handleSearch} className="space-y-4">
              <div className="flex flex-col md:flex-row gap-4">
                <Select value={inputType} onValueChange={setInputType}>
                  <SelectTrigger className="w-full md:w-48" data-testid="input-type-select">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="domain">Domain</SelectItem>
                    <SelectItem value="company_name">Company Name</SelectItem>
                    <SelectItem value="linkedin_url">LinkedIn URL</SelectItem>
                  </SelectContent>
                </Select>
                <Input
                  type="text"
                  placeholder={inputType === 'domain' ? 'example.com' : inputType === 'company_name' ? 'Company Name' : 'LinkedIn URL'}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  className="flex-1"
                  data-testid="search-input"
                />
                <Button 
                  type="submit" 
                  disabled={loading}
                  className="bg-emerald-600 hover:bg-emerald-700 gap-2"
                  data-testid="search-button"
                >
                  <Search className="w-5 h-5" />
                  {loading ? 'Searching...' : 'Search'}
                </Button>
              </div>
            </form>
            <p className="text-sm text-gray-500 mt-4">Free plan includes 10 searches. No credit card required.</p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">Why CorpInfo?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-8 border border-gray-200 rounded-xl card-hover" data-testid="feature-speed">
              <Zap className="w-12 h-12 text-emerald-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Lightning Fast</h3>
              <p className="text-gray-600">Get results in 5-15 seconds. Our AI-powered crawler processes multiple sources simultaneously.</p>
            </div>
            <div className="p-8 border border-gray-200 rounded-xl card-hover">
              <Shield className="w-12 h-12 text-emerald-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Verified Data</h3>
              <p className="text-gray-600">Confidence scoring on every result. We prioritize official sources and cross-verify information.</p>
            </div>
            <div className="p-8 border border-gray-200 rounded-xl card-hover">
              <TrendingUp className="w-12 h-12 text-emerald-600 mb-4" />
              <h3 className="text-xl font-semibold mb-3">Scalable</h3>
              <p className="text-gray-600">Bulk upload CSVs with thousands of companies. Maintain sequence and export enriched data.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4 bg-emerald-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Research?</h2>
          <p className="text-xl text-gray-600 mb-8">Start with 10 free searches. No credit card required.</p>
          <Button 
            size="lg" 
            className="bg-emerald-600 hover:bg-emerald-700 gap-2"
            onClick={() => navigate(isAuthenticated ? '/dashboard' : '/register')}
            data-testid="cta-button"
          >
            Get Started Free
            <ArrowRight className="w-5 h-5" />
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;
