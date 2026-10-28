// CI_PAGES_URL supports both project paths and GitLab Pages unique domains.
function getDeploymentConfig(env = {}) {
  const target = env.PAGES_URL || env.CI_PAGES_URL || 'http://localhost:3000/';
  const parsed = new URL(target);
  if (!['https:', 'http:'].includes(parsed.protocol)) {
    throw new Error('Pages URL must use HTTP or HTTPS');
  }
  const pathname = parsed.pathname.replace(/\/+$/, '');
  return {url: parsed.origin, baseUrl: `${pathname}/`, trailingSlash: true};
}
module.exports = {getDeploymentConfig};
