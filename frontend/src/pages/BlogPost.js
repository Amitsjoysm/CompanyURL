import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { content } from '../utils/api';
import { Button } from '../components/ui/button';
import { ArrowLeft, Loader2 } from 'lucide-react';

const BlogPost = () => {
  const { slug } = useParams();
  const [blog, setBlog] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBlog();
  }, [slug]);

  const loadBlog = async () => {
    try {
      const response = await content.getBlog(slug);
      setBlog(response.data);
    } catch (error) {
      console.error('Failed to load blog');
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

  if (!blog) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Blog not found</h2>
          <Link to="/blogs">
            <Button>Back to Blogs</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <article className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-8 md:p-12">
        <Link to="/blogs">
          <Button variant="ghost" className="mb-8 gap-2" data-testid="back-button">
            <ArrowLeft className="w-4 h-4" />
            Back to Blog
          </Button>
        </Link>

        <header className="mb-8">
          <h1 className="text-4xl md:text-5xl font-bold mb-4" data-testid="blog-title">{blog.title}</h1>
          <div className="flex items-center text-gray-600">
            <span>By {blog.author}</span>
            <span className="mx-2">•</span>
            <time>{new Date(blog.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</time>
          </div>
        </header>

        <div className="prose prose-lg max-w-none" data-testid="blog-content">
          {blog.content.split('\n').map((paragraph, idx) => {
            if (paragraph.startsWith('## ')) {
              return <h2 key={idx} className="text-2xl font-bold mt-8 mb-4">{paragraph.replace('## ', '')}</h2>;
            } else if (paragraph.startsWith('### ')) {
              return <h3 key={idx} className="text-xl font-semibold mt-6 mb-3">{paragraph.replace('### ', '')}</h3>;
            } else if (paragraph.trim()) {
              return <p key={idx} className="mb-4 text-gray-700 leading-relaxed">{paragraph}</p>;
            }
            return null;
          })}
        </div>
      </article>
    </div>
  );
};

export default BlogPost;
