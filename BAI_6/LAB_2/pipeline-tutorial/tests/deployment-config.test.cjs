const {test} = require('node:test');
const assert = require('node:assert/strict');
const {getDeploymentConfig} = require('../scripts/deployment-config.cjs');

test('local preview uses the root path', () => {
  assert.deepEqual(getDeploymentConfig(), {url: 'http://localhost:3000', baseUrl: '/', trailingSlash: true});
});
test('GitLab project and nested namespace paths keep their base path', () => {
  assert.equal(getDeploymentConfig({CI_PAGES_URL: 'https://student.gitlab.io/group/lab-06'}).baseUrl, '/group/lab-06/');
});
test('unique domain uses the root path', () => {
  assert.equal(getDeploymentConfig({CI_PAGES_URL: 'https://lab-06-123.gitlab.io/'}).baseUrl, '/');
});
test('explicit Pages URL overrides CI and normalizes trailing slashes', () => {
  assert.equal(getDeploymentConfig({PAGES_URL: 'https://example.com/lab///', CI_PAGES_URL: 'https://other.test/'}).baseUrl, '/lab/');
});
test('rejects a non-web deployment URL', () => {
  assert.throws(() => getDeploymentConfig({PAGES_URL: 'file:///lab'}), /HTTP/);
});
