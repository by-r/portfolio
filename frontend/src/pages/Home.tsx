import { Link } from "react-router-dom";
import { Button, LayerCard } from "@cloudflare/kumo";
import { ArrowRight, GithubLogo } from "@phosphor-icons/react";

const highlights = ["Django & django-ninja", "React + TypeScript", "Tailwind CSS v4", "Kumo UI"];

export default function Home() {
  return (
    <section className="space-y-10 py-10">
      <LayerCard className="rounded-2xl p-8 sm:p-10">
        <p className="text-sm font-medium uppercase tracking-widest text-blue-600">
          Hello, I&apos;m
        </p>
        <h1 className="mt-2 text-4xl font-bold tracking-tight sm:text-5xl">
          Jane Doe
        </h1>
        <p className="mt-4 max-w-xl text-lg leading-7 text-zinc-600">
          I build simple, secure software. This is my little corner of the web —
          a portfolio and a blog about the things I&apos;m learning.
        </p>
        <div className="mt-8 flex flex-wrap items-center gap-3">
          <Link to="/blog">
            <Button variant="primary">
              Read the blog <ArrowRight weight="bold" />
            </Button>
          </Link>
          <a
            href="https://github.com/example"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Button variant="secondary">
              <GithubLogo weight="fill" /> GitHub
            </Button>
          </a>
        </div>
      </LayerCard>

      <div>
        <h2 className="text-sm font-medium uppercase tracking-widest text-zinc-400">
          Currently exploring
        </h2>
        <ul className="mt-4 flex flex-wrap gap-2">
          {highlights.map((item) => (
            <li
              key={item}
              className="rounded-full border border-zinc-200 bg-white px-3 py-1 text-sm text-zinc-600"
            >
              {item}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
