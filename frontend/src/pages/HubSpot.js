import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Badge } from '../components/ui/badge';
import { Switch } from '../components/ui/switch';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import { hubspot, crawl } from '../utils/api';
import { Link2, Link2Off, RefreshCw, Settings, CheckCircle, AlertCircle, Upload, Zap } from 'lucide-react';

const HubSpot = () => {
  const [loading, setLoading] = useState(true);
  const [connectionStatus, setConnectionStatus] = useState(null);
  const [settings, setSettings] = useState(null);
  const [syncing, setSyncing] = useState(false);
  const [companies, setCompanies] = useState([]);
  const [selectedCompanies, setSelectedCompanies] = useState([]);

  useEffect(() => {
    loadStatus();
    loadSettings();
    loadCompanies();
  }, []);

  const loadStatus = async () => {
    try {
      const response = await hubspot.getStatus();
      setConnectionStatus(response.data);
    } catch (error) {
      console.error('Failed to load status:', error);
      if (error.response?.status === 403) {
        toast.error('HubSpot CRM is only available for Enterprise users');
      }
    } finally {
      setLoading(false);
    }
  };

  const loadSettings = async () => {
    try {
      const response = await hubspot.getSettings();
      setSettings(response.data);
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  };

  const loadCompanies = async () => {
    try {
      const response = await crawl.getHistory();
      // Filter only completed requests with results
      const completedCompanies = response.data
        .filter(req => req.status === 'completed' && req.result)
        .map(req => ({
          id: req.id,
          name: req.result.company_name || req.input_value,
          domain: req.result.domain || req.input_value,
          linkedin_url: req.result.linkedin_url,
          industry: req.result.industry,
          company_size: req.result.company_size,
          description: req.result.description,
        }));
      setCompanies(completedCompanies);
    } catch (error) {
      console.error('Failed to load companies:', error);
    }
  };

  const handleConnect = async () => {
    try {
      const response = await hubspot.getAuthUrl();
      window.location.href = response.data.auth_url;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to get authorization URL');
    }
  };

  const handleDisconnect = async () => {
    if (!window.confirm('Are you sure you want to disconnect HubSpot?')) {
      return;
    }

    try {
      await hubspot.disconnect();
      toast.success('HubSpot disconnected successfully');
      loadStatus();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to disconnect');
    }
  };

  const handleSettingsUpdate = async (field, value) => {
    try {
      const updatedSettings = { ...settings, [field]: value };
      await hubspot.updateSettings(updatedSettings);
      setSettings(updatedSettings);
      toast.success('Settings updated');
    } catch (error) {
      toast.error('Failed to update settings');
    }
  };

  const handleSyncCompanies = async () => {
    if (selectedCompanies.length === 0) {
      toast.error('Please select companies to sync');
      return;
    }

    try {
      setSyncing(true);
      const companiesToSync = companies
        .filter(c => selectedCompanies.includes(c.id))
        .map(c => ({
          name: c.name,
          domain: c.domain,
          linkedin_url: c.linkedin_url,
          industry: c.industry,
          company_size: c.company_size,
          description: c.description,
        }));

      const response = await hubspot.syncCompanies(companiesToSync);
      toast.success(`Synced ${response.data.successful} companies successfully`);
      if (response.data.failed > 0) {
        toast.warning(`${response.data.failed} companies failed to sync`);
      }
      setSelectedCompanies([]);
      loadSettings();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Sync failed');
    } finally {
      setSyncing(false);
    }
  };

  const toggleCompanySelection = (id) => {
    setSelectedCompanies(prev =>
      prev.includes(id) ? prev.filter(cid => cid !== id) : [...prev, id]
    );
  };

  const selectAll = () => {
    if (selectedCompanies.length === companies.length) {
      setSelectedCompanies([]);
    } else {
      setSelectedCompanies(companies.map(c => c.id));
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto text-gray-400 mb-2" />
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <img src="https://www.hubspot.com/hubfs/HubSpot_Logos/HubSpot-Inversed-Favicon.png" alt="HubSpot" className="w-8 h-8" />
            HubSpot CRM Integration
          </h1>
          <p className="text-gray-600 mt-1">Sync your company data to HubSpot CRM</p>
        </div>

        {/* Connection Status */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {connectionStatus?.connected ? (
                <>
                  <Link2 className="w-5 h-5 text-green-600" />
                  Connected
                </>
              ) : (
                <>
                  <Link2Off className="w-5 h-5 text-gray-400" />
                  Not Connected
                </>
              )}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {connectionStatus?.connected ? (
              <>
                <Alert className="bg-green-50 border-green-200">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <AlertDescription className="text-green-800">
                    Your HubSpot account is connected and ready to sync data.
                  </AlertDescription>
                </Alert>

                {settings?.last_sync_at && (
                  <p className="text-sm text-gray-600">
                    Last synced: {new Date(settings.last_sync_at).toLocaleString()}
                  </p>
                )}

                <Button variant="destructive" onClick={handleDisconnect}>
                  <Link2Off className="w-4 h-4 mr-2" />
                  Disconnect HubSpot
                </Button>
              </>
            ) : (
              <>
                <Alert>
                  <AlertCircle className="w-4 h-4" />
                  <AlertDescription>
                    Connect your HubSpot account to sync company data from your crawl results to HubSpot CRM.
                  </AlertDescription>
                </Alert>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-900 mb-2">What you'll get:</h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>✓ Automatic company data sync to HubSpot</li>
                    <li>✓ Keep your CRM up to date with enriched company information</li>
                    <li>✓ Manual or automatic sync options</li>
                    <li>✓ Bulk sync multiple companies at once</li>
                  </ul>
                </div>

                <Button onClick={handleConnect} className="w-full">
                  <Link2 className="w-4 h-4 mr-2" />
                  Connect to HubSpot
                </Button>
              </>
            )}
          </CardContent>
        </Card>

        {/* Settings (only if connected) */}
        {connectionStatus?.connected && settings && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5" />
                Sync Settings
              </CardTitle>
              <CardDescription>Configure how data syncs to HubSpot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">Auto Sync</Label>
                  <p className="text-sm text-gray-600">Automatically sync new crawl results to HubSpot</p>
                </div>
                <Switch
                  checked={settings.auto_sync_enabled}
                  onCheckedChange={(checked) => handleSettingsUpdate('auto_sync_enabled', checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">Sync Companies</Label>
                  <p className="text-sm text-gray-600">Include company information in sync</p>
                </div>
                <Switch
                  checked={settings.sync_companies}
                  onCheckedChange={(checked) => handleSettingsUpdate('sync_companies', checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-base font-medium">Sync Contacts</Label>
                  <p className="text-sm text-gray-600">Include contact information in sync</p>
                </div>
                <Switch
                  checked={settings.sync_contacts}
                  onCheckedChange={(checked) => handleSettingsUpdate('sync_contacts', checked)}
                />
              </div>
            </CardContent>
          </Card>
        )}

        {/* Manual Sync (only if connected) */}
        {connectionStatus?.connected && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Manual Sync
              </CardTitle>
              <CardDescription>Select companies to sync to HubSpot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {companies.length === 0 ? (
                <p className="text-center text-gray-500 py-8">
                  No completed crawl results available. Complete some crawl requests first.
                </p>
              ) : (
                <>
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-gray-600">
                      {selectedCompanies.length} of {companies.length} companies selected
                    </p>
                    <Button variant="outline" size="sm" onClick={selectAll}>
                      {selectedCompanies.length === companies.length ? 'Deselect All' : 'Select All'}
                    </Button>
                  </div>

                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {companies.map((company) => (
                      <div
                        key={company.id}
                        className={`p-3 border rounded-lg cursor-pointer transition ${
                          selectedCompanies.includes(company.id)
                            ? 'border-emerald-500 bg-emerald-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                        onClick={() => toggleCompanySelection(company.id)}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <h4 className="font-semibold">{company.name}</h4>
                            <p className="text-sm text-gray-600">{company.domain}</p>
                          </div>
                          <input
                            type="checkbox"
                            checked={selectedCompanies.includes(company.id)}
                            onChange={() => toggleCompanySelection(company.id)}
                            className="w-5 h-5 text-emerald-600 rounded focus:ring-emerald-500"
                          />
                        </div>
                      </div>
                    ))}
                  </div>

                  <Button
                    onClick={handleSyncCompanies}
                    disabled={selectedCompanies.length === 0 || syncing}
                    className="w-full bg-emerald-600 hover:bg-emerald-700"
                  >
                    {syncing ? (
                      <>
                        <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                        Syncing...
                      </>
                    ) : (
                      <>
                        <Zap className="w-4 h-4 mr-2" />
                        Sync {selectedCompanies.length} Companies to HubSpot
                      </>
                    )}
                  </Button>
                </>
              )}
            </CardContent>
          </Card>
        )}

        {/* Info Banner */}
        <Alert className="bg-blue-50 border-blue-200">
          <AlertCircle className="w-4 h-4 text-blue-600" />
          <AlertDescription className="text-blue-800">
            <strong>Enterprise Feature:</strong> HubSpot CRM integration is available for Enterprise plan users.
            Upgrade your plan to access this feature.
          </AlertDescription>
        </Alert>
      </div>
    </div>
  );
};

export default HubSpot;
