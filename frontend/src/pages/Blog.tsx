import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { LayerCard } from "@cloudflare/kumo";
import { api, type PostSummary } from "../lib/api";
import { formatDate } from "../lib/format";

export default function Blog() {
  const [posts, setPosts] = useState<PostSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listPosts()
      .then(setPosts)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : String(e)));
  }, []);

  return (
    <section className="space-y-6 py-10">
      <h1 className="text-3xl font-bold tracking-tight">Blog</h1>

      {error && <p className="text-red-600">Failed to load posts: {error}</p>}
      {!posts && !error && <p className="text-zinc-500">Loading…</p>}
      {posts && posts.length === 0 && (
        <p className="text-zinc-500">No posts yet — check back soon.</p>
      )}

      {posts?.map((post) => (
        <Link key={post.slug} to={`/blog/${post.slug}`} className="block">
          <LayerCard className="rounded-2xl p-6 transition-shadow hover:shadow-md">
            <h2 className="text-xl font-semibold tracking-tight">{post.title}</h2>
            <p className="mt-1 text-sm text-zinc-500">
              {formatDate(post.created_at)}
            </p>
            <p className="mt-3 leading-6 text-zinc-600">{post.excerpt}</p>
          </LayerCard>
        </Link>
      ))}
    </section>
  );
}
