# Docusaurus - Bài thực hành 6

Đây là mã nguồn website của [Lab 2](../README.md).

```powershell
npm.cmd ci
npm.cmd test
npm.cmd run build
npm.cmd run serve
```

Đưa nội dung thư mục này vào gốc dự án GitLab để chạy pipeline.
`.gitlab-ci.yml` là bản hai stage build/deploy đã triển khai.
`ci/06-build-test-deploy.gitlab-ci.yml` là bản mở rộng có thêm stage test.

Website: https://lab-06-devsecops-58b0f2.gitlab.io/
