import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from 'sonner';
import { crawl } from '../utils/api';
import { Search, Upload, History, Loader2, CheckCircle, XCircle, Clock, Eye } from 'lucide-react';
import { useDropzone } from 'react-dropzone';

const Dashboard = () => {
  const { user, updateCredits } = useAuth();
  const navigate = useNavigate();
  const [inputType, setInputType] = useState('domain');
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [requests, setRequests] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await crawl.getHistory();
      setRequests(response.data);
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) {
      toast.error('Please enter a value');
      return;
    }

    try {
      setLoading(true);
      const response = await crawl.single({ input_type: inputType, input_value: inputValue });
      toast.success('Crawl request created!');
      setInputValue('');
      loadHistory();
      updateCredits(user.credits - 1);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create request');
    } finally {
      setLoading(false);
    }
  };

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('input_type', inputType);

      toast.info('Uploading file...');
      const response = await crawl.bulkUpload(formData);
      toast.success(response.data.message);
      loadHistory();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Upload failed');
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'], 'application/vnd.ms-excel': ['.xls', '.xlsx'] },
    maxFiles: 1,
  });

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'failed': return <XCircle className="w-5 h-5 text-red-600" />;
      case 'processing': return <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />;
      default: return <Clock className="w-5 h-5 text-gray-600" />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold" data-testid="dashboard-title">Dashboard</h1>
          <p className="text-gray-600 mt-2">Credits: <span className="font-semibold" data-testid="credits-display">{user?.credits || 0}</span></p>
        </div>

        {/* Search */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="w-5 h-5" />
              Single Search
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4">
              <Select value={inputType} onValueChange={setInputType}>
                <SelectTrigger className="w-full md:w-48">
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
                placeholder="Enter value..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                className="flex-1"
                data-testid="dashboard-search-input"
              />
              <Button type="submit" disabled={loading} data-testid="dashboard-search-button">
                {loading ? 'Searching...' : 'Search'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Bulk Upload */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="w-5 h-5" />
              Bulk Upload
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
                isDragActive ? 'border-emerald-500 bg-emerald-50' : 'border-gray-300 hover:border-emerald-400'
              }`}
              data-testid="dropzone"
            >
              <input {...getInputProps()} />
              <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-600">
                {isDragActive ? 'Drop file here' : 'Drag & drop CSV/Excel or click to browse'}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* History */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <History className="w-5 h-5" />
              Recent Requests
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loadingHistory ? (
              <div className="text-center py-8">
                <Loader2 className="w-8 h-8 animate-spin mx-auto text-gray-400" />
              </div>
            ) : requests.length === 0 ? (
              <p className="text-center text-gray-500 py-8">No requests yet</p>
            ) : (
              <div className="space-y-3">
                {requests.map((req) => (
                  <div
                    key={req.id}
                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition"
                    data-testid="request-item"
                  >
                    <div className="flex items-center gap-4 flex-1">
                      {getStatusIcon(req.status)}
                      <div className="flex-1">
                        <p className="font-medium">{req.input_value}</p>
                        <p className="text-sm text-gray-500">{req.input_type}</p>
                      </div>
                      {req.result?.confidence_score && (
                        <div className="text-sm">
                          <span className="font-medium">Confidence: </span>
                          <span className={req.result.confidence_score > 0.7 ? 'text-green-600' : 'text-yellow-600'}>
                            {(req.result.confidence_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
