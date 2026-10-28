const {getDeploymentConfig} = require('./scripts/deployment-config.cjs');

module.exports = {
  title: 'Bài 6 · DevSecOps',
  tagline: 'Tích hợp bảo mật trong quy trình CI/CD',
  ...getDeploymentConfig(process.env),
  onBrokenLinks: 'throw',
  i18n: {defaultLocale: 'vi', locales: ['vi']},
  presets: [
    ['classic', {
      docs: {sidebarPath: require.resolve('./sidebars.js')},
      blog: false,
      theme: {customCss: require.resolve('./src/css/custom.css')},
    }],
  ],
  themeConfig: {
    navbar: {
      title: 'LAB / 06',
      items: [
        {to: '/docs/intro', label: 'Bài thực hành', position: 'left'},
        {to: '/docs/security', label: 'Bảo mật', position: 'left'},
        {to: '/docs/submission', label: 'Nộp bài', position: 'right'},
      ],
    },
    footer: {
      style: 'dark',
      copyright: 'Bài thực hành 6 — Bảo mật với DevSecOps',
    },
  },
};
