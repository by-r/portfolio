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

const API_BASE = import.meta.env.VITE_API_URL || "/api";

async function get<T>(path: string): Promise<T> {
  const url = `${API_BASE}${path}`;

  try {
    const res = await fetch(url);

    if (!res.ok) {
      const body = await res.text();
      const detail = body ? ` — ${body.slice(0, 300)}` : "";
      throw new Error(`API request failed (${res.status} ${res.statusText}) at ${url}${detail}`);
    }

    return (await res.json()) as T;
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        `API request could not reach ${url}. Check that Django is running and the API URL/proxy is configured.`,
      );
    }

    throw error;
  }
}

export const api = {
  listPosts: () => get<PostSummary[]>("/posts"),
  getPost: (slug: string) =>
    get<PostDetail>(`/posts/${encodeURIComponent(slug)}`),
};
