---
title: 6.2.2 — Docusaurus và GitLab Pages
sidebar_position: 3
---

# Pipeline build và triển khai

Dự án Docusaurus đã nằm ngay tại thư mục gốc, không cần tạo thêm `website/`.

## Các bước tăng dần

Chọn lần lượt các tệp làm **CI/CD configuration file**, chạy pipeline và chụp log tương ứng:

1. `ci/02-first-job.gitlab-ci.yml`: một job in thông báo và ngày giờ.
2. `ci/03-build.gitlab-ci.yml`: cài thư viện bằng `npm ci`, build rồi lưu artifact `build/`.
3. `ci/04-build-deploy.gitlab-ci.yml`: hai stage build và deploy đúng cấu trúc phần cuối đề.
4. `ci/06-build-test-deploy.gitlab-ci.yml`: bản mở rộng thêm stage test trước deploy.

## Bản đang triển khai

| Stage | Job | Kết quả |
| --- | --- | --- |
| build | build-job | `npm ci`, `npm run build`, lưu `build/` |
| deploy | pages | Tải artifact build, chuyển thành `public/`, xuất bản Pages |

Pipeline minh chứng dùng hai stage build/deploy; cả build-job, pages và pages:deploy đã thành công trong pipeline #2997205623. Job deploy chỉ chạy trên nhánh mặc định. Bản mở rộng ba stage ở `ci/06-build-test-deploy.gitlab-ci.yml` thêm kiểm thử bắt buộc trước deploy.

## URL và baseUrl

`docusaurus.config.js` sử dụng URL theo thứ tự:

1. Biến `PAGES_URL` nếu tự đặt trong GitLab CI/CD Variables.
2. Biến dựng sẵn `CI_PAGES_URL` từ GitLab.
3. `http://localhost:3000/` khi chạy tại máy.

Ví dụ URL `https://student.gitlab.io/lab-06/` tạo `url = https://student.gitlab.io`, `baseUrl = /lab-06/`. URL dạng unique domain dùng `baseUrl = /`.

Nếu thay đổi unique domain sau lần build, cần chạy lại pipeline để sinh đường dẫn đúng. Với domain riêng, đặt `PAGES_URL` bằng URL HTTPS đầy đủ của website.

## Xem kết quả

Vào **Deploy → Pages** và mở URL do GitLab cung cấp. Kiểm tra trang chủ, tài liệu và CSS. Không cần tắt unique domain; nếu muốn URL theo mẫu trong PDF, tắt tùy chọn đó rồi chạy lại pipeline.

Cấu hình có `pages.publish: public` theo cú pháp hiện hành của GitLab. Tên job vẫn giữ `pages` để dễ đối chiếu đề.
