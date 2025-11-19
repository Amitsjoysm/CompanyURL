import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { content } from '../utils/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { ArrowRight, Loader2 } from 'lucide-react';

const Blogs = () => {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBlogs();
  }, []);

  const loadBlogs = async () => {
    try {
      const response = await content.getBlogs();
      setBlogs(response.data);
    } catch (error) {
      console.error('Failed to load blogs');
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

  return (
    <div className="min-h-screen bg-gray-50 py-20 px-4">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-4" data-testid="blogs-title">Blog</h1>
          <p className="text-xl text-gray-600">Insights, guides, and best practices for company research</p>
        </div>

        <div className="space-y-8">
          {blogs.map((blog) => (
            <Link key={blog.id} to={`/blog/${blog.slug}`} data-testid="blog-item">
              <Card className="hover:shadow-lg transition card-hover">
                <CardHeader>
                  <CardTitle className="text-2xl">{blog.title}</CardTitle>
                  <CardDescription className="text-base">
                    {blog.excerpt || blog.content.substring(0, 200) + '...'}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">
                      By {blog.author} • {new Date(blog.created_at).toLocaleDateString()}
                    </span>
                    <ArrowRight className="w-5 h-5 text-emerald-600" />
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Blogs;
