import React, { useState, useEffect } from 'react';
import { content } from '../utils/api';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../components/ui/accordion';
import { Loader2 } from 'lucide-react';

const FAQ = () => {
  const [faqs, setFaqs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFaqs();
  }, []);

  const loadFaqs = async () => {
    try {
      const response = await content.getFaqs();
      setFaqs(response.data);
    } catch (error) {
      console.error('Failed to load FAQs');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
      </div>
    );
  }

  const categories = [...new Set(faqs.map(f => f.category).filter(Boolean))];

  return (
    <div className="min-h-screen bg-gray-50 py-20 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-4" data-testid="faq-title">Frequently Asked Questions</h1>
          <p className="text-xl text-gray-600">Everything you need to know about CorpInfo</p>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-8">
          {categories.length > 0 ? (
            categories.map(category => (
              <div key={category} className="mb-8 last:mb-0">
                <h2 className="text-2xl font-bold mb-4 text-emerald-600">{category}</h2>
                <Accordion type="single" collapsible className="space-y-4">
                  {faqs.filter(f => f.category === category).map((faq) => (
                    <AccordionItem key={faq.id} value={faq.id} data-testid="faq-item">
                      <AccordionTrigger className="text-left font-medium text-lg">
                        {faq.question}
                      </AccordionTrigger>
                      <AccordionContent className="text-gray-700 leading-relaxed">
                        {faq.answer}
                      </AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </div>
            ))
          ) : (
            <Accordion type="single" collapsible className="space-y-4">
              {faqs.map((faq) => (
                <AccordionItem key={faq.id} value={faq.id} data-testid="faq-item">
                  <AccordionTrigger className="text-left font-medium text-lg">
                    {faq.question}
                  </AccordionTrigger>
                  <AccordionContent className="text-gray-700 leading-relaxed">
                    {faq.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          )}
        </div>
      </div>
    </div>
  );
};

export default FAQ;
