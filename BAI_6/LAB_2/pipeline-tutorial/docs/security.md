---
title: 6.1 — Bảo mật trong CI/CD
sidebar_position: 4
---

# Tích hợp bảo mật với DevSecOps

## Thiết kế pipeline an toàn

| Biện pháp | Áp dụng cho dự án |
| --- | --- |
| Quyền tối thiểu | Phân quyền thành viên, bảo vệ nhánh mặc định, bật MFA trong tài khoản GitLab |
| Quản lý secrets | Lưu khóa trong CI/CD Variables hoặc vault, bật masked/protected khi phù hợp; không commit `.env` |
| Tính toàn vẹn | Commit lockfile, dùng `npm ci`; chữ ký commit và artifact cần cấu hình khóa và chính sách xác minh riêng |
| Security gates | Không dùng `allow_failure` cho kiểm tra bắt buộc; deploy chạy sau test |
| Audit | Lưu job logs, artifacts; rà soát thay đổi `.gitlab-ci.yml` qua merge request |
| Runner | Dùng runner cô lập, cập nhật thường xuyên, tránh privileged mode khi không cần |

MFA, bảo vệ nhánh, phê duyệt merge request và ký commit cần được cấu hình trên tài khoản/kho GitLab; các tệp cục bộ không tự bật các chính sách đó.

## Phân biệt các loại kiểm tra

- **SAST:** phân tích mã nguồn, ví dụ tìm luồng dữ liệu gây injection. Có thể bổ sung GitLab SAST hoặc Semgrep khi có quy tắc phù hợp.
- **DAST:** quét ứng dụng đang chạy, ví dụ OWASP ZAP trên môi trường staging được phép kiểm tra.
- **SCA:** đối chiếu dependency với cơ sở dữ liệu lỗ hổng, ở đây dùng `npm audit`.
- **Secret scanning:** tìm thông tin xác thực bị commit, ở bản mở rộng dùng Trivy.
- **IaC scanning:** kiểm tra cấu hình hạ tầng như Terraform, Kubernetes hoặc Dockerfile. Trivy có scanner misconfiguration; dự án hiện chưa có IaC/container nên không có tài nguyên loại này để đánh giá.

## Chạy bản mở rộng

Đặt **CI/CD configuration file** thành `ci/05-devsecops.gitlab-ci.yml`. Tệp này include pipeline gốc và thêm hai job ở stage test:

```text
build → [test-job, dependency-scan, config-and-secret-scan] → pages
```

`dependency-scan` chạy `npm audit --omit=dev --audit-level=high`. Trivy quét dependency, secret và misconfiguration; trả exit code 1 khi có phát hiện HIGH/CRITICAL. Các gate này không thay thế SAST hoặc DAST. Trivy cần tải image và cơ sở dữ liệu qua mạng; lỗi tải cũng làm job thất bại.

Nếu có phát hiện, kiểm tra advisory, cập nhật thư viện hoặc sửa cấu hình rồi chạy lại. Không tắt gate chỉ để pipeline xanh. Với dependency gián tiếp, kiểm tra gói cha và dùng cập nhật tương thích; không tự động chạy `npm audit fix --force`.

`npm audit --omit=dev` bao gồm các dependency build được khai báo trong dự án; các package này không trở thành server Node.js sau khi triển khai. Pages chỉ phục vụ file tĩnh, nhưng rủi ro trong công cụ build vẫn cần được đánh giá.

## Giới hạn

Bản mở rộng là ví dụ có thể chạy thêm, không phải bằng chứng hệ thống đã được kiểm toán bảo mật. Chưa triển khai vault, ký số, DAST, quét container hay hạ tầng thật vì bài hiện tại chỉ có website tĩnh và chưa có các môi trường tương ứng.
