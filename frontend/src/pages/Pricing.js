import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Slider } from '../components/ui/slider';
import { Check } from 'lucide-react';
import { payment } from '../utils/api';
import { toast } from 'sonner';

const Pricing = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [enterpriseCredits, setEnterpriseCredits] = useState([5000]);

  useEffect(() => {
    loadPlans();
  }, []);

  const loadPlans = async () => {
    try {
      const response = await payment.getPlans();
      setPlans(response.data);
    } catch (error) {
      console.error('Failed to load plans');
    }
  };

  const calculateEnterprisePrice = (credits) => {
    const baseRate = 49 / 2500; // Pro plan rate
    const discount = Math.min(credits / 100000, 0.3); // Up to 30% discount
    return (credits * baseRate * (1 - discount)).toFixed(2);
  };

  const handlePurchase = async (planName, price, credits) => {
    if (!isAuthenticated) {
      toast.error('Please login to purchase');
      navigate('/login');
      return;
    }

    try {
      const keyResponse = await payment.getRazorpayKey();
      const razorpayKey = keyResponse.data.key;

      if (!razorpayKey) {
        toast.error('Payment system not configured. Please contact support.');
        return;
      }

      const orderResponse = await payment.createOrder({ plan_name: planName, amount: price, credits });
      const order = orderResponse.data;

      const options = {
        key: razorpayKey,
        amount: price * 100,
        currency: 'INR',
        name: 'CorpInfo',
        description: `${planName} Plan`,
        order_id: order.razorpay_order_id,
        handler: async function (response) {
          try {
            await payment.verify({
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
              transaction_id: order.id,
            });
            toast.success('Payment successful! Credits added.');
            window.location.reload();
          } catch (error) {
            toast.error('Payment verification failed');
          }
        },
      };

      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (error) {
      toast.error('Failed to create order');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-4" data-testid="pricing-title">Simple, Transparent Pricing</h1>
          <p className="text-xl text-gray-600">Choose the plan that fits your needs</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {/* Free */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle>Free</CardTitle>
              <CardDescription>Perfect for trying out</CardDescription>
              <div className="mt-4">
                <span className="text-4xl font-bold">$0</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <ul className="space-y-3">
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>10 searches</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>Basic features</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>Community support</span>
                </li>
              </ul>
              <Button className="w-full" variant="outline" onClick={() => navigate('/register')} data-testid="free-plan-button">
                Get Started
              </Button>
            </CardContent>
          </Card>

          {/* Starter */}
          <Card className="border-2 border-emerald-500 relative">
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span className="bg-emerald-500 text-white px-4 py-1 rounded-full text-sm font-medium">Popular</span>
            </div>
            <CardHeader>
              <CardTitle>Starter</CardTitle>
              <CardDescription>For growing teams</CardDescription>
              <div className="mt-4">
                <span className="text-4xl font-bold">$25</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <ul className="space-y-3">
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>1,000 searches</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>Bulk upload</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>Priority processing</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>Email support</span>
                </li>
              </ul>
              <Button 
                className="w-full bg-emerald-600 hover:bg-emerald-700" 
                onClick={() => handlePurchase('Starter', 25, 1000)}
                data-testid="starter-plan-button"
              >
                Purchase
              </Button>
            </CardContent>
          </Card>

          {/* Pro */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle>Pro</CardTitle>
              <CardDescription>For power users</CardDescription>
              <div className="mt-4">
                <span className="text-4xl font-bold">$49</span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <ul className="space-y-3">
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>2,500 searches</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>API access</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>Advanced features</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  <span>Priority support</span>
                </li>
              </ul>
              <Button 
                className="w-full" 
                onClick={() => handlePurchase('Pro', 49, 2500)}
                data-testid="pro-plan-button"
              >
                Purchase
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Enterprise */}
        <Card className="max-w-3xl mx-auto">
          <CardHeader>
            <CardTitle>Enterprise</CardTitle>
            <CardDescription>Custom volume with discounts</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <div className="flex justify-between mb-4">
                <span className="font-medium">Credits: {enterpriseCredits[0].toLocaleString()}</span>
                <span className="text-2xl font-bold">${calculateEnterprisePrice(enterpriseCredits[0])}</span>
              </div>
              <Slider
                value={enterpriseCredits}
                onValueChange={setEnterpriseCredits}
                min={5000}
                max={1000000}
                step={5000}
                className="mb-2"
              />
              <p className="text-sm text-gray-500">Lower per-credit cost as volume increases</p>
            </div>
            <Button 
              className="w-full bg-emerald-600 hover:bg-emerald-700"
              onClick={() => handlePurchase('Enterprise', parseFloat(calculateEnterprisePrice(enterpriseCredits[0])), enterpriseCredits[0])}
              data-testid="enterprise-plan-button"
            >
              Purchase Enterprise
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Pricing;
