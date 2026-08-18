import React from "react";
import {
  BrowserRouter,
  Link as RouterLink,
  Route,
  Routes,
} from "react-router-dom";
import { LinkProvider } from "@cloudflare/kumo";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Blog from "./pages/Blog";
import BlogPost from "./pages/BlogPost";

type AppLinkProps = React.AnchorHTMLAttributes<HTMLAnchorElement> & {
  to?: string;
};

// Adapter: Kumo's LinkProvider renders its components with `href`; react-router
// Link navigates via `to`. Map href → to so Kumo links use the router.
const AppLink = React.forwardRef<HTMLAnchorElement, AppLinkProps>(
  ({ href, to, ...rest }, ref) => (
    <RouterLink ref={ref} to={href ?? to ?? "#"} {...rest} />
  )
);

export default function App() {
  return (
    // Tell Kumo's Link component to use react-router navigation.
    <LinkProvider component={AppLink}>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="blog" element={<Blog />} />
            <Route path="blog/:slug" element={<BlogPost />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </LinkProvider>
  );
}
