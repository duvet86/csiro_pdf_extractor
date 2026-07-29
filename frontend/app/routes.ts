import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("/summary", "routes/job-summary.tsx"),
] satisfies RouteConfig;
