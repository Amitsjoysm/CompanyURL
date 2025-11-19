import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { toast } from 'sonner';
import { crawl } from '../utils/api';
import { ArrowLeft, Loader2, CheckCircle, XCircle, Clock, Building, Globe, Linkedin, MapPin, Users, Calendar, Phone, Mail, Twitter, Facebook, TrendingUp } from 'lucide-react';

const RequestDetail = () => {
  const { requestId } = useParams();
  const navigate = useNavigate();
  const [request, setRequest] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRequest();
  }, [requestId]);

  const loadRequest = async () => {
    try {
      const response = await crawl.getRequest(requestId);
      setRequest(response.data);
    } catch (error) {
      toast.error('Failed to load request details');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-6 h-6 text-green-600" />;
      case 'failed':
        return <XCircle className="w-6 h-6 text-red-600" />;
      case 'processing':
        return <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />;
      default:
        return <Clock className="w-6 h-6 text-gray-600" />;
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      completed: 'bg-green-100 text-green-700',
      failed: 'bg-red-100 text-red-700',
      processing: 'bg-blue-100 text-blue-700',
      pending: 'bg-yellow-100 text-yellow-700',
    };
    return <Badge className={variants[status] || variants.pending}>{status}</Badge>;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-12 h-12 animate-spin text-gray-400" />
      </div>
    );
  }

  if (!request) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Request not found</h2>
          <Button onClick={() => navigate('/dashboard')} className="mt-4">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  const result = request.result;

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <Button variant="ghost" onClick={() => navigate('/dashboard')}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <div className="flex-1">
            <h1 className="text-3xl font-bold">Request Details</h1>
          </div>
        </div>

        {/* Request Info */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span className="flex items-center gap-3">
                {getStatusIcon(request.status)}
                {request.input_value}
              </span>
              {getStatusBadge(request.status)}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-600">Input Type</p>
                <p className="font-medium capitalize">{request.input_type.replace('_', ' ')}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Created At</p>
                <p className="font-medium">{new Date(request.created_at).toLocaleString()}</p>
              </div>
              {request.completed_at && (
                <div>
                  <p className="text-sm text-gray-600">Completed At</p>
                  <p className="font-medium">{new Date(request.completed_at).toLocaleString()}</p>
                </div>
              )}
            </div>
            {result?.confidence_score !== undefined && (
              <div>
                <p className="text-sm text-gray-600">Confidence Score</p>
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        result.confidence_score > 0.7 ? 'bg-green-600' :
                        result.confidence_score > 0.4 ? 'bg-yellow-600' : 'bg-red-600'
                      }`}
                      style={{ width: `${result.confidence_score * 100}%` }}
                    />
                  </div>
                  <span className="font-semibold">{(result.confidence_score * 100).toFixed(0)}%</span>
                </div>
              </div>
            )}
            {request.error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm font-medium text-red-800">Error</p>
                <p className="text-sm text-red-600 mt-1">{request.error}</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Company Data */}
        {result && (
          <>
            {/* Basic Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Building className="w-5 h-5" />
                  Company Information
                </CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {result.company_name && (
                  <div>
                    <p className="text-sm text-gray-600 flex items-center gap-2">
                      <Building className="w-4 h-4" />
                      Company Name
                    </p>
                    <p className="font-medium text-lg">{result.company_name}</p>
                  </div>
                )}
                {result.domain && (
                  <div>
                    <p className="text-sm text-gray-600 flex items-center gap-2">
                      <Globe className="w-4 h-4" />
                      Domain
                    </p>
                    <a href={`https://${result.domain}`} target="_blank" rel="noopener noreferrer" className="font-medium text-blue-600 hover:underline">
                      {result.domain}
                    </a>
                  </div>
                )}
                {result.linkedin_url && (
                  <div>
                    <p className="text-sm text-gray-600 flex items-center gap-2">
                      <Linkedin className="w-4 h-4" />
                      LinkedIn URL
                    </p>
                    <a href={result.linkedin_url} target="_blank" rel="noopener noreferrer" className="font-medium text-blue-600 hover:underline truncate block">
                      {result.linkedin_url}
                    </a>
                  </div>
                )}
                {result.industry && (
                  <div>
                    <p className="text-sm text-gray-600">Industry</p>
                    <p className="font-medium">{result.industry}</p>
                  </div>
                )}
                {result.employee_size && (
                  <div>
                    <p className="text-sm text-gray-600 flex items-center gap-2">
                      <Users className="w-4 h-4" />
                      Employee Size
                    </p>
                    <p className="font-medium">{result.employee_size}</p>
                  </div>
                )}
                {result.founded_on && (
                  <div>
                    <p className="text-sm text-gray-600 flex items-center gap-2">
                      <Calendar className="w-4 h-4" />
                      Founded
                    </p>
                    <p className="font-medium">{result.founded_on}</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Description */}
            {result.description && (
              <Card>
                <CardHeader>
                  <CardTitle>About</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed">{result.description}</p>
                </CardContent>
              </Card>
            )}

            {/* Contact Information */}
            {(result.address || result.phone_numbers?.length || result.emails?.length || result.location || result.country) && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <MapPin className="w-5 h-5" />
                    Contact Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {result.address && (
                    <div>
                      <p className="text-sm text-gray-600">Address</p>
                      <p className="font-medium">{result.address}</p>
                    </div>
                  )}
                  {result.location && (
                    <div>
                      <p className="text-sm text-gray-600">Location</p>
                      <p className="font-medium">{result.location}</p>
                    </div>
                  )}
                  {result.country && (
                    <div>
                      <p className="text-sm text-gray-600">Country</p>
                      <p className="font-medium">{result.country}</p>
                    </div>
                  )}
                  {result.phone_numbers?.length > 0 && (
                    <div>
                      <p className="text-sm text-gray-600 flex items-center gap-2">
                        <Phone className="w-4 h-4" />
                        Phone Numbers
                      </p>
                      {result.phone_numbers.map((phone, idx) => (
                        <p key={idx} className="font-medium">{phone}</p>
                      ))}
                    </div>
                  )}
                  {result.emails?.length > 0 && (
                    <div>
                      <p className="text-sm text-gray-600 flex items-center gap-2">
                        <Mail className="w-4 h-4" />
                        Emails
                      </p>
                      {result.emails.map((email, idx) => (
                        <a key={idx} href={`mailto:${email}`} className="font-medium text-blue-600 hover:underline block">
                          {email}
                        </a>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Social Media */}
            {(result.twitter_url || result.facebook_url) && (
              <Card>
                <CardHeader>
                  <CardTitle>Social Media</CardTitle>
                </CardHeader>
                <CardContent className="flex gap-4">
                  {result.twitter_url && (
                    <a href={result.twitter_url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-blue-600 hover:underline">
                      <Twitter className="w-5 h-5" />
                      Twitter
                    </a>
                  )}
                  {result.facebook_url && (
                    <a href={result.facebook_url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-blue-600 hover:underline">
                      <Facebook className="w-5 h-5" />
                      Facebook
                    </a>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Founders */}
            {result.founders?.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Founders</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {result.founders.map((founder, idx) => (
                      <Badge key={idx} variant="secondary" className="text-sm">{founder}</Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Latest News */}
            {result.latest_news?.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5" />
                    Latest News
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {result.latest_news.map((news, idx) => (
                    <div key={idx} className="border-l-4 border-emerald-500 pl-4">
                      <h4 className="font-semibold">{news.title || 'News Item'}</h4>
                      {news.description && <p className="text-sm text-gray-600 mt-1">{news.description}</p>}
                      {news.url && (
                        <a href={news.url} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 hover:underline mt-1 inline-block">
                          Read more →
                        </a>
                      )}
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Data Sources */}
            {result.data_sources?.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Data Sources</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {result.data_sources.map((source, idx) => (
                      <Badge key={idx} variant="outline">{source}</Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default RequestDetail;
