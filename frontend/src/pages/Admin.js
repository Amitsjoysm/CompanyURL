import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from 'sonner';
import { admin, content, payment, crawl } from '../utils/api';
import { Shield, Users, CreditCard, FileText, HelpCircle, Database, Loader2, Pencil, Trash2, Plus } from 'lucide-react';

const Admin = () => {
  const { user, isSuperadmin } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('users');
  const [loading, setLoading] = useState(false);

  // States for different sections
  const [users, setUsers] = useState([]);
  const [plans, setPlans] = useState([]);
  const [blogs, setBlogs] = useState([]);
  const [faqs, setFaqs] = useState([]);
  const [ledger, setLedger] = useState([]);

  // Redirect if not superadmin
  useEffect(() => {
    if (!isSuperadmin) {
      toast.error('Access denied. Superadmin only.');
      navigate('/dashboard');
    }
  }, [isSuperadmin, navigate]);

  // Load data based on active tab
  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    setLoading(true);
    try {
      switch (activeTab) {
        case 'users':
          const usersRes = await admin.getUsers();
          setUsers(usersRes.data);
          break;
        case 'plans':
          const plansRes = await payment.getPlans();
          setPlans(plansRes.data);
          break;
        case 'blogs':
          const blogsRes = await content.getBlogs();
          setBlogs(blogsRes.data);
          break;
        case 'faqs':
          const faqsRes = await content.getFaqs();
          setFaqs(faqsRes.data);
          break;
        case 'ledger':
          const ledgerRes = await admin.getCentralLedger();
          setLedger(ledgerRes.data);
          break;
        default:
          break;
      }
    } catch (error) {
      console.error('Failed to load data:', error);
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  if (!isSuperadmin) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <Shield className="w-8 h-8 text-emerald-600" />
              Admin Dashboard
            </h1>
            <p className="text-gray-600 mt-1">Manage users, plans, content, and system data</p>
          </div>
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid grid-cols-5 w-full">
            <TabsTrigger value="users" className="gap-2">
              <Users className="w-4 h-4" />
              Users
            </TabsTrigger>
            <TabsTrigger value="plans" className="gap-2">
              <CreditCard className="w-4 h-4" />
              Plans
            </TabsTrigger>
            <TabsTrigger value="blogs" className="gap-2">
              <FileText className="w-4 h-4" />
              Blogs
            </TabsTrigger>
            <TabsTrigger value="faqs" className="gap-2">
              <HelpCircle className="w-4 h-4" />
              FAQs
            </TabsTrigger>
            <TabsTrigger value="ledger" className="gap-2">
              <Database className="w-4 h-4" />
              Ledger
            </TabsTrigger>
          </TabsList>

          {/* Users Tab */}
          <TabsContent value="users">
            <UsersManager users={users} loadData={loadData} loading={loading} />
          </TabsContent>

          {/* Plans Tab */}
          <TabsContent value="plans">
            <PlansManager plans={plans} loadData={loadData} loading={loading} />
          </TabsContent>

          {/* Blogs Tab */}
          <TabsContent value="blogs">
            <BlogsManager blogs={blogs} loadData={loadData} loading={loading} />
          </TabsContent>

          {/* FAQs Tab */}
          <TabsContent value="faqs">
            <FAQsManager faqs={faqs} loadData={loadData} loading={loading} />
          </TabsContent>

          {/* Central Ledger Tab */}
          <TabsContent value="ledger">
            <LedgerViewer ledger={ledger} loading={loading} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

// Users Manager Component
const UsersManager = ({ users, loadData, loading }) => {
  const [editingUser, setEditingUser] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  const handleUpdateCredits = async (userId, newCredits) => {
    try {
      await admin.updateUserCredits(userId, { credits: newCredits });
      toast.success('Credits updated successfully');
      loadData();
    } catch (error) {
      toast.error('Failed to update credits');
    }
  };

  const handleToggleStatus = async (userId, isActive) => {
    try {
      await admin.updateUserStatus(userId, { is_active: !isActive });
      toast.success(`User ${!isActive ? 'activated' : 'deactivated'} successfully`);
      loadData();
    } catch (error) {
      toast.error('Failed to update user status');
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>User Management</CardTitle>
        <CardDescription>Manage user accounts, credits, and permissions</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
          </div>
        ) : users.length === 0 ? (
          <p className="text-center text-gray-500 py-8">No users found</p>
        ) : (
          <div className="space-y-4">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4">Email</th>
                    <th className="text-left py-3 px-4">Name</th>
                    <th className="text-left py-3 px-4">Role</th>
                    <th className="text-left py-3 px-4">Credits</th>
                    <th className="text-left py-3 px-4">Status</th>
                    <th className="text-left py-3 px-4">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id} className="border-b hover:bg-gray-50">
                      <td className="py-3 px-4">{user.email}</td>
                      <td className="py-3 px-4">{user.full_name || '-'}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs ${
                          user.role === 'superadmin' ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-700'
                        }`}>
                          {user.role}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-semibold">{user.credits}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded text-xs ${
                          user.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                        }`}>
                          {user.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex gap-2">
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button variant="outline" size="sm">
                                <Pencil className="w-4 h-4" />
                              </Button>
                            </DialogTrigger>
                            <DialogContent>
                              <DialogHeader>
                                <DialogTitle>Edit User Credits</DialogTitle>
                              </DialogHeader>
                              <EditUserForm user={user} onSave={(credits) => {
                                handleUpdateCredits(user.id, credits);
                              }} />
                            </DialogContent>
                          </Dialog>
                          <Button 
                            variant={user.is_active ? "destructive" : "default"} 
                            size="sm"
                            onClick={() => handleToggleStatus(user.id, user.is_active)}
                          >
                            {user.is_active ? 'Deactivate' : 'Activate'}
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

const EditUserForm = ({ user, onSave }) => {
  const [credits, setCredits] = useState(user.credits);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(parseInt(credits));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label>Credits</Label>
        <Input
          type="number"
          value={credits}
          onChange={(e) => setCredits(e.target.value)}
          min="0"
        />
      </div>
      <Button type="submit">Save Changes</Button>
    </form>
  );
};

// Plans Manager Component
const PlansManager = ({ plans, loadData, loading }) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingPlan, setEditingPlan] = useState(null);

  const handleDelete = async (planId) => {
    if (!window.confirm('Are you sure you want to delete this plan?')) return;
    
    try {
      await admin.deletePlan(planId);
      toast.success('Plan deleted successfully');
      loadData();
    } catch (error) {
      toast.error('Failed to delete plan');
    }
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>Plans Management</CardTitle>
          <CardDescription>Manage pricing plans and credits</CardDescription>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => setEditingPlan(null)}>
              <Plus className="w-4 h-4 mr-2" />
              Add Plan
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>{editingPlan ? 'Edit Plan' : 'Create Plan'}</DialogTitle>
            </DialogHeader>
            <PlanForm plan={editingPlan} onSuccess={() => {
              setDialogOpen(false);
              loadData();
            }} />
          </DialogContent>
        </Dialog>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
          </div>
        ) : plans.length === 0 ? (
          <p className="text-center text-gray-500 py-8">No plans found</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {plans.map((plan) => (
              <Card key={plan.id} className="border-2">
                <CardHeader>
                  <CardTitle className="text-xl">{plan.name}</CardTitle>
                  <div className="text-3xl font-bold text-emerald-600">
                    ${plan.price}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <p className="text-sm text-gray-600">Credits</p>
                    <p className="text-2xl font-semibold">{plan.credits.toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Status</p>
                    <span className={`px-2 py-1 rounded text-xs ${
                      plan.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                      {plan.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  <div className="flex gap-2 pt-4">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="flex-1"
                      onClick={() => {
                        setEditingPlan(plan);
                        setDialogOpen(true);
                      }}
                    >
                      <Pencil className="w-4 h-4 mr-2" />
                      Edit
                    </Button>
                    <Button 
                      variant="destructive" 
                      size="sm"
                      onClick={() => handleDelete(plan.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

const PlanForm = ({ plan, onSuccess }) => {
  const [formData, setFormData] = useState({
    name: plan?.name || '',
    price: plan?.price || 0,
    credits: plan?.credits || 0,
    is_active: plan?.is_active !== undefined ? plan.is_active : true,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (plan) {
        await admin.updatePlan(plan.id, formData);
        toast.success('Plan updated successfully');
      } else {
        await admin.createPlan(formData);
        toast.success('Plan created successfully');
      }
      onSuccess();
    } catch (error) {
      toast.error(`Failed to ${plan ? 'update' : 'create'} plan`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label>Plan Name</Label>
        <Input
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          placeholder="e.g., Starter, Pro, Enterprise"
          required
        />
      </div>
      <div>
        <Label>Price ($)</Label>
        <Input
          type="number"
          value={formData.price}
          onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) })}
          min="0"
          step="0.01"
          required
        />
      </div>
      <div>
        <Label>Credits</Label>
        <Input
          type="number"
          value={formData.credits}
          onChange={(e) => setFormData({ ...formData, credits: parseInt(e.target.value) })}
          min="0"
          required
        />
      </div>
      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          id="is_active"
          checked={formData.is_active}
          onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
        />
        <Label htmlFor="is_active">Active</Label>
      </div>
      <Button type="submit">{plan ? 'Update' : 'Create'} Plan</Button>
    </form>
  );
};

// Blogs Manager Component
const BlogsManager = ({ blogs, loadData, loading }) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingBlog, setEditingBlog] = useState(null);

  const handleDelete = async (slug) => {
    if (!window.confirm('Are you sure you want to delete this blog?')) return;
    
    try {
      await content.deleteBlog(slug);
      toast.success('Blog deleted successfully');
      loadData();
    } catch (error) {
      toast.error('Failed to delete blog');
    }
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>Blogs Management</CardTitle>
          <CardDescription>Create and manage blog posts</CardDescription>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => setEditingBlog(null)}>
              <Plus className="w-4 h-4 mr-2" />
              Add Blog
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{editingBlog ? 'Edit Blog' : 'Create Blog'}</DialogTitle>
            </DialogHeader>
            <BlogForm blog={editingBlog} onSuccess={() => {
              setDialogOpen(false);
              loadData();
            }} />
          </DialogContent>
        </Dialog>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
          </div>
        ) : blogs.length === 0 ? (
          <p className="text-center text-gray-500 py-8">No blogs found</p>
        ) : (
          <div className="space-y-4">
            {blogs.map((blog) => (
              <Card key={blog.id}>
                <CardContent className="p-4">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">{blog.title}</h3>
                      <p className="text-sm text-gray-600 mt-1">{blog.excerpt}</p>
                      <div className="flex gap-4 mt-2 text-xs text-gray-500">
                        <span>Slug: {blog.slug}</span>
                        <span className={`px-2 py-1 rounded ${
                          blog.is_published ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                        }`}>
                          {blog.is_published ? 'Published' : 'Draft'}
                        </span>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => {
                          setEditingBlog(blog);
                          setDialogOpen(true);
                        }}
                      >
                        <Pencil className="w-4 h-4" />
                      </Button>
                      <Button 
                        variant="destructive" 
                        size="sm"
                        onClick={() => handleDelete(blog.slug)}
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
  );
};

const BlogForm = ({ blog, onSuccess }) => {
  const [formData, setFormData] = useState({
    title: blog?.title || '',
    slug: blog?.slug || '',
    excerpt: blog?.excerpt || '',
    content: blog?.content || '',
    author: blog?.author || 'Admin',
    is_published: blog?.is_published !== undefined ? blog.is_published : true,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (blog) {
        await content.updateBlog(blog.slug, formData);
        toast.success('Blog updated successfully');
      } else {
        await content.createBlog(formData);
        toast.success('Blog created successfully');
      }
      onSuccess();
    } catch (error) {
      toast.error(`Failed to ${blog ? 'update' : 'create'} blog`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label>Title</Label>
        <Input
          value={formData.title}
          onChange={(e) => {
            const title = e.target.value;
            const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-');
            setFormData({ ...formData, title, slug });
          }}
          placeholder="Blog title"
          required
        />
      </div>
      <div>
        <Label>Slug</Label>
        <Input
          value={formData.slug}
          onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
          placeholder="blog-url-slug"
          required
        />
      </div>
      <div>
        <Label>Excerpt</Label>
        <Textarea
          value={formData.excerpt}
          onChange={(e) => setFormData({ ...formData, excerpt: e.target.value })}
          placeholder="Short description"
          rows={2}
          required
        />
      </div>
      <div>
        <Label>Content</Label>
        <Textarea
          value={formData.content}
          onChange={(e) => setFormData({ ...formData, content: e.target.value })}
          placeholder="Full blog content"
          rows={10}
          required
        />
      </div>
      <div>
        <Label>Author</Label>
        <Input
          value={formData.author}
          onChange={(e) => setFormData({ ...formData, author: e.target.value })}
          placeholder="Author name"
          required
        />
      </div>
      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          id="is_published"
          checked={formData.is_published}
          onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
        />
        <Label htmlFor="is_published">Published</Label>
      </div>
      <Button type="submit">{blog ? 'Update' : 'Create'} Blog</Button>
    </form>
  );
};

// FAQs Manager Component
const FAQsManager = ({ faqs, loadData, loading }) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingFaq, setEditingFaq] = useState(null);

  const handleDelete = async (faqId) => {
    if (!window.confirm('Are you sure you want to delete this FAQ?')) return;
    
    try {
      await content.deleteFaq(faqId);
      toast.success('FAQ deleted successfully');
      loadData();
    } catch (error) {
      toast.error('Failed to delete FAQ');
    }
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>FAQs Management</CardTitle>
          <CardDescription>Manage frequently asked questions</CardDescription>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => setEditingFaq(null)}>
              <Plus className="w-4 h-4 mr-2" />
              Add FAQ
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>{editingFaq ? 'Edit FAQ' : 'Create FAQ'}</DialogTitle>
            </DialogHeader>
            <FAQForm faq={editingFaq} onSuccess={() => {
              setDialogOpen(false);
              loadData();
            }} />
          </DialogContent>
        </Dialog>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
          </div>
        ) : faqs.length === 0 ? (
          <p className="text-center text-gray-500 py-8">No FAQs found</p>
        ) : (
          <div className="space-y-4">
            {faqs.map((faq) => (
              <Card key={faq.id}>
                <CardContent className="p-4">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold">{faq.question}</h3>
                      <p className="text-sm text-gray-600 mt-1">{faq.answer}</p>
                      <div className="mt-2">
                        <span className={`px-2 py-1 rounded text-xs ${
                          faq.is_published ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                        }`}>
                          {faq.is_published ? 'Published' : 'Draft'}
                        </span>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => {
                          setEditingFaq(faq);
                          setDialogOpen(true);
                        }}
                      >
                        <Pencil className="w-4 h-4" />
                      </Button>
                      <Button 
                        variant="destructive" 
                        size="sm"
                        onClick={() => handleDelete(faq.id)}
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
  );
};

const FAQForm = ({ faq, onSuccess }) => {
  const [formData, setFormData] = useState({
    question: faq?.question || '',
    answer: faq?.answer || '',
    category: faq?.category || 'general',
    is_published: faq?.is_published !== undefined ? faq.is_published : true,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (faq) {
        await content.updateFaq(faq.id, formData);
        toast.success('FAQ updated successfully');
      } else {
        await content.createFaq(formData);
        toast.success('FAQ created successfully');
      }
      onSuccess();
    } catch (error) {
      toast.error(`Failed to ${faq ? 'update' : 'create'} FAQ`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label>Question</Label>
        <Input
          value={formData.question}
          onChange={(e) => setFormData({ ...formData, question: e.target.value })}
          placeholder="What is your question?"
          required
        />
      </div>
      <div>
        <Label>Answer</Label>
        <Textarea
          value={formData.answer}
          onChange={(e) => setFormData({ ...formData, answer: e.target.value })}
          placeholder="Answer to the question"
          rows={4}
          required
        />
      </div>
      <div>
        <Label>Category</Label>
        <Select value={formData.category} onValueChange={(value) => setFormData({ ...formData, category: value })}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="general">General</SelectItem>
            <SelectItem value="pricing">Pricing</SelectItem>
            <SelectItem value="technical">Technical</SelectItem>
            <SelectItem value="account">Account</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          id="faq_published"
          checked={formData.is_published}
          onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
        />
        <Label htmlFor="faq_published">Published</Label>
      </div>
      <Button type="submit">{faq ? 'Update' : 'Create'} FAQ</Button>
    </form>
  );
};

// Central Ledger Viewer Component
const LedgerViewer = ({ ledger, loading }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Central Company Ledger</CardTitle>
        <CardDescription>All crawled company data across all users</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
          </div>
        ) : ledger.length === 0 ? (
          <p className="text-center text-gray-500 py-8">No data in ledger yet</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4">Company</th>
                  <th className="text-left py-3 px-4">Domain</th>
                  <th className="text-left py-3 px-4">LinkedIn</th>
                  <th className="text-left py-3 px-4">Industry</th>
                  <th className="text-left py-3 px-4">Confidence</th>
                  <th className="text-left py-3 px-4">Last Crawled</th>
                </tr>
              </thead>
              <tbody>
                {ledger.map((company) => (
                  <tr key={company.id} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-4 font-medium">{company.company_name || '-'}</td>
                    <td className="py-3 px-4">{company.domain || '-'}</td>
                    <td className="py-3 px-4 truncate max-w-xs">
                      {company.linkedin_url ? (
                        <a href={company.linkedin_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                          {company.linkedin_url.substring(0, 40)}...
                        </a>
                      ) : '-'}
                    </td>
                    <td className="py-3 px-4">{company.industry || '-'}</td>
                    <td className="py-3 px-4">
                      <span className={`font-semibold ${
                        company.confidence_score > 0.7 ? 'text-green-600' : 
                        company.confidence_score > 0.4 ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {(company.confidence_score * 100).toFixed(0)}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-xs">
                      {new Date(company.last_crawled).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default Admin;
