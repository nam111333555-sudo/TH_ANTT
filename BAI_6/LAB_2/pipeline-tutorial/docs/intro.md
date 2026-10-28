---
title: Tổng quan bài thực hành
sidebar_position: 1
---

# Bài 6: Bảo mật với DevSecOps

Mục tiêu: thiết kế pipeline CI/CD, hiểu các chốt kiểm tra bảo mật và triển khai một website Docusaurus bằng GitLab Pages.

## Nội dung đã chuẩn bị

| Phần trong đề | Tệp thực hiện |
| --- | --- |
| 6.1 — Bảo mật CI/CD | Tài liệu Bảo mật và pipeline mở rộng `ci/05-devsecops.gitlab-ci.yml` |
| 6.2.1 — Bốn job cơ bản | `ci/01-basic.gitlab-ci.yml` |
| 6.2.2 — Job đầu tiên | `ci/02-first-job.gitlab-ci.yml` |
| 6.2.2 — Build Docusaurus | `ci/03-build.gitlab-ci.yml` |
| 6.2.2 — Build và Pages, hai stage | `ci/04-build-deploy.gitlab-ci.yml` |
| Pipeline hai stage đang triển khai | `.gitlab-ci.yml` |
| Bản mở rộng thêm stage test | `ci/06-build-test-deploy.gitlab-ci.yml` |

## Chạy tại máy

Yêu cầu Node.js 22 trở lên và npm. Từ thư mục chứa `package.json`:

```bash
npm ci
npm test
npm run build
npm run serve
```

Lệnh cuối phục vụ thư mục `build/` tại địa chỉ được in ra trong terminal. Trong PowerShell, nếu `npm.ps1` bị chặn, dùng `npm.cmd` thay cho `npm`.

Để chỉnh sửa và xem thay đổi trực tiếp, chạy `npm start`.

## Artifact là gì?

Artifact là kết quả job được GitLab lưu để tải về hoặc truyền sang job sau. Ở bài này, `build-job` tạo `build/`; job `pages` tải artifact đó, đổi tên thành `public/` và phát hành website.

Website này không tự xác nhận pipeline đã thành công. Cần chạy trên GitLab và thu thập minh chứng theo trang Nộp bài.
