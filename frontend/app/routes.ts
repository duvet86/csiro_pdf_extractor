import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("/summary", "routes/job-summary.tsx"),
  route("/job-details/:jobId", "routes/job-details.tsx"),
] satisfies RouteConfig;
