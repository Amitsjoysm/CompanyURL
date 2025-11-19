import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Badge } from '../components/ui/badge';
import { toast } from 'sonner';
import { apiTokens } from '../utils/api';
import { Key, Copy, Trash2, Power, Plus, AlertCircle, CheckCircle2, Book } from 'lucide-react';

const APITokens = () => {
  const [tokens, setTokens] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [newToken, setNewToken] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    expires_in_days: 90,
  });

  useEffect(() => {
    loadTokens();
  }, []);

  const loadTokens = async () => {
    try {
      const response = await apiTokens.list();
      setTokens(response.data);
    } catch (error) {
      toast.error('Failed to load API tokens');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    
    try {
      const response = await apiTokens.create(formData);
      setNewToken(response.data);
      setFormData({ name: '', expires_in_days: 90 });
      loadTokens();
      toast.success('API token created successfully');
    } catch (error) {
      toast.error('Failed to create token');
    }
  };

  const handleRevoke = async (tokenId) => {
    if (!window.confirm('Are you sure you want to revoke this token? This action cannot be undone.')) {
      return;
    }

    try {
      await apiTokens.revoke(tokenId);
      toast.success('Token revoked successfully');
      loadTokens();
    } catch (error) {
      toast.error('Failed to revoke token');
    }
  };

  const handleToggle = async (tokenId) => {
    try {
      await apiTokens.toggle(tokenId);
      toast.success('Token status updated');
      loadTokens();
    } catch (error) {
      toast.error('Failed to update token status');
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard');
  };

  const closeNewTokenDialog = () => {
    setNewToken(null);
    setDialogOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <Key className="w-8 h-8 text-emerald-600" />
              API Tokens
            </h1>
            <p className="text-gray-600 mt-1">Manage API tokens for programmatic access</p>
          </div>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => setNewToken(null)}>
                <Plus className="w-4 h-4 mr-2" />
                Generate Token
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Generate New API Token</DialogTitle>
              </DialogHeader>
              {newToken ? (
                <NewTokenDisplay token={newToken} onClose={closeNewTokenDialog} />
              ) : (
                <TokenForm formData={formData} setFormData={setFormData} onSubmit={handleCreate} />
              )}
            </DialogContent>
          </Dialog>
        </div>

        {/* Documentation Alert */}
        <Alert className="bg-blue-50 border-blue-200">
          <Book className="w-4 h-4 text-blue-600" />
          <AlertDescription className="text-blue-800">
            <strong>Need help?</strong> Check out the{' '}
            <a href="/API_USAGE_GUIDE.md" target="_blank" className="underline font-medium">
              API Usage Guide
            </a>
            {' '}and{' '}
            <a href="/MCP_SERVER_SETUP.md" target="_blank" className="underline font-medium">
              MCP Server Setup
            </a>
            {' '}documentation.
          </AlertDescription>
        </Alert>

        {/* Quick Start Guide */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Start</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold">
                    1
                  </div>
                  <h3 className="font-semibold">Generate Token</h3>
                </div>
                <p className="text-sm text-gray-600">
                  Click "Generate Token" and give it a descriptive name
                </p>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold">
                    2
                  </div>
                  <h3 className="font-semibold">Copy Token</h3>
                </div>
                <p className="text-sm text-gray-600">
                  Save the token immediately (shown only once)
                </p>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold">
                    3
                  </div>
                  <h3 className="font-semibold">Use in API</h3>
                </div>
                <p className="text-sm text-gray-600">
                  Add header: <code className="text-xs bg-gray-100 px-1 py-0.5 rounded">X-API-Key: your_token</code>
                </p>
              </div>
            </div>
            
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm font-medium mb-2">Example API Request:</p>
              <code className="text-xs bg-gray-800 text-green-400 p-3 rounded block overflow-x-auto">
                curl -H "X-API-Key: corp_your_token_here" \<br/>
                &nbsp;&nbsp;https://sync-dashboard-2.preview.emergentagent.com/api/crawl/history
              </code>
            </div>
          </CardContent>
        </Card>

        {/* Tokens List */}
        <Card>
          <CardHeader>
            <CardTitle>Your API Tokens</CardTitle>
            <CardDescription>Active and inactive tokens for API access</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8 text-gray-500">Loading tokens...</div>
            ) : tokens.length === 0 ? (
              <div className="text-center py-12">
                <Key className="w-16 h-16 mx-auto text-gray-300 mb-4" />
                <p className="text-gray-500 mb-4">No API tokens yet</p>
                <Button onClick={() => setDialogOpen(true)}>
                  <Plus className="w-4 h-4 mr-2" />
                  Generate Your First Token
                </Button>
              </div>
            ) : (
              <div className="space-y-3">
                {tokens.map((token) => (
                  <Card key={token.id} className="border">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <h3 className="font-semibold text-lg">{token.name}</h3>
                            <Badge className={token.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'}>
                              {token.is_active ? 'Active' : 'Inactive'}
                            </Badge>
                          </div>
                          <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                              <span className="text-gray-600">Token:</span>
                              <code className="ml-2 bg-gray-100 px-2 py-1 rounded text-xs">
                                {token.token_preview}
                              </code>
                            </div>
                            <div>
                              <span className="text-gray-600">Created:</span>
                              <span className="ml-2">{new Date(token.created_at).toLocaleDateString()}</span>
                            </div>
                            {token.last_used && (
                              <div>
                                <span className="text-gray-600">Last Used:</span>
                                <span className="ml-2">{new Date(token.last_used).toLocaleDateString()}</span>
                              </div>
                            )}
                            {token.expires_at && (
                              <div>
                                <span className="text-gray-600">Expires:</span>
                                <span className="ml-2">{new Date(token.expires_at).toLocaleDateString()}</span>
                              </div>
                            )}
                          </div>
                          <div className="mt-2">
                            <span className="text-xs text-gray-600">Scopes:</span>
                            {token.scopes.map((scope) => (
                              <Badge key={scope} variant="outline" className="ml-2 text-xs">
                                {scope}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        <div className="flex gap-2 ml-4">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleToggle(token.id)}
                            title={token.is_active ? 'Disable' : 'Enable'}
                          >
                            <Power className={`w-4 h-4 ${token.is_active ? 'text-green-600' : 'text-gray-400'}`} />
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => handleRevoke(token.id)}
                            title="Revoke"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Security Best Practices */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-yellow-600" />
              Security Best Practices
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                <span>Store tokens in environment variables, never in code</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                <span>Use separate tokens for development, staging, and production</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                <span>Rotate tokens regularly (every 90 days recommended)</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                <span>Revoke tokens immediately if compromised</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                <span>Never share tokens or commit them to version control</span>
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

const TokenForm = ({ formData, setFormData, onSubmit }) => {
  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div>
        <Label>Token Name</Label>
        <Input
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          placeholder="e.g., Production API, MCP Server"
          required
        />
        <p className="text-xs text-gray-500 mt-1">
          Give your token a descriptive name to identify its purpose
        </p>
      </div>
      
      <div>
        <Label>Expires In (Days)</Label>
        <Input
          type="number"
          value={formData.expires_in_days}
          onChange={(e) => setFormData({ ...formData, expires_in_days: parseInt(e.target.value) || 90 })}
          min="1"
          max="365"
        />
        <p className="text-xs text-gray-500 mt-1">
          Recommended: 90 days. Leave blank for no expiration.
        </p>
      </div>

      <Alert>
        <AlertCircle className="w-4 h-4" />
        <AlertDescription className="text-sm">
          <strong>Important:</strong> The token will only be shown once. Save it securely immediately after creation.
        </AlertDescription>
      </Alert>

      <Button type="submit" className="w-full">
        Generate Token
      </Button>
    </form>
  );
};

const NewTokenDisplay = ({ token, onClose }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(token.token);
    setCopied(true);
    toast.success('Token copied to clipboard');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-4">
      <Alert className="bg-green-50 border-green-200">
        <CheckCircle2 className="w-4 h-4 text-green-600" />
        <AlertDescription className="text-green-800">
          <strong>Token created successfully!</strong> Make sure to copy it now. You won't be able to see it again.
        </AlertDescription>
      </Alert>

      <div>
        <Label>Your API Token</Label>
        <div className="flex gap-2 mt-2">
          <Input
            value={token.token}
            readOnly
            className="font-mono text-sm"
          />
          <Button onClick={handleCopy} variant="outline">
            {copied ? <CheckCircle2 className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
          </Button>
        </div>
      </div>

      <div className="bg-gray-50 p-4 rounded-lg">
        <p className="text-sm font-medium mb-2">Use in your API requests:</p>
        <code className="text-xs bg-gray-800 text-green-400 p-3 rounded block overflow-x-auto">
          curl -H "X-API-Key: {token.token}" \<br/>
          &nbsp;&nbsp;https://sync-dashboard-2.preview.emergentagent.com/api/crawl/history
        </code>
      </div>

      <Alert>
        <AlertCircle className="w-4 h-4 text-yellow-600" />
        <AlertDescription className="text-sm">
          Store this token securely. It provides full access to your account via API.
        </AlertDescription>
      </Alert>

      <Button onClick={onClose} className="w-full">
        Done
      </Button>
    </div>
  );
};

export default APITokens;
