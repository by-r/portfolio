export interface PostSummary {
  title: string;
  slug: string;
  excerpt: string;
  created_at: string;
  updated_at: string;
}

export interface PostDetail extends PostSummary {
  content: string;
}

const API_BASE: string = import.meta.env.VITE_API_URL || "/api";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API request failed: ${res.status} ${res.statusText}`);
  }
  return (await res.json()) as T;
}

export const api = {
  listPosts: () => get<PostSummary[]>("/posts"),
  getPost: (slug: string) =>
    get<PostDetail>(`/posts/${encodeURIComponent(slug)}`),
};
