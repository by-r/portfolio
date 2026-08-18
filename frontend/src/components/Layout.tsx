import { Link, NavLink, Outlet } from "react-router-dom";

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `text-sm font-medium transition-colors ${
    isActive ? "text-zinc-900" : "text-zinc-500 hover:text-zinc-900"
  }`;

export default function Layout() {
  return (
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col px-6">
      <header className="flex items-center justify-between py-8">
        <Link to="/" className="text-lg font-semibold tracking-tight">
          Jane Doe
        </Link>
        <nav className="flex items-center gap-6">
          <NavLink to="/" end className={navLinkClass}>
            Home
          </NavLink>
          <NavLink to="/blog" className={navLinkClass}>
            Blog
          </NavLink>
        </nav>
      </header>
      <main className="flex-1">
        <Outlet />
      </main>
      <footer className="py-8 text-sm text-zinc-400">
        © {new Date().getFullYear()} · Built with Django-Ninja, React &amp; Kumo
        UI
      </footer>
    </div>
  );
}
