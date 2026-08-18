import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { api, type PostDetail } from "../lib/api";
import { formatDate } from "../lib/format";

export default function BlogPost() {
  const { slug } = useParams<{ slug: string }>();
  const [post, setPost] = useState<PostDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    setPost(null);
    setError(null);
    api
      .getPost(slug)
      .then(setPost)
      .catch((e: unknown) =>
        setError(e instanceof Error ? e.message : String(e))
      );
  }, [slug]);

  if (error) {
    return (
      <div className="py-10">
        <p className="text-red-600">Could not load this post.</p>
        <Link to="/blog" className="mt-4 inline-block text-blue-600 underline">
          ← Back to blog
        </Link>
      </div>
    );
  }

  if (!post) {
    return <p className="py-10 text-zinc-500">Loading…</p>;
  }

  return (
    <article className="py-10">
      <Link
        to="/blog"
        className="text-sm text-zinc-500 transition-colors hover:text-zinc-900"
      >
        ← Back to blog
      </Link>
      <h1 className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl">
        {post.title}
      </h1>
      <p className="mt-2 text-sm text-zinc-500">{formatDate(post.created_at)}</p>
      <div className="markdown-body mt-6">
        {/* react-markdown escapes raw HTML by default — safe rendering */}
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{post.content}</ReactMarkdown>
      </div>
    </article>
  );
}
