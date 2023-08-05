
// prefer default export if available
const preferDefault = m => (m && m.default) || m


exports.components = {
  "component---src-pages-404-tsx": preferDefault(require("/home/victordibia/projects/peacasso/peacasso/web/frontend/src/pages/404.tsx")),
  "component---src-pages-index-tsx": preferDefault(require("/home/victordibia/projects/peacasso/peacasso/web/frontend/src/pages/index.tsx")),
  "component---src-pages-login-tsx": preferDefault(require("/home/victordibia/projects/peacasso/peacasso/web/frontend/src/pages/login.tsx"))
}

