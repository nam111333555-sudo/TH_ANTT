---
title: 6.2.1 — Pipeline cơ bản
sidebar_position: 2
---

# Tạo và chạy pipeline đầu tiên

Sử dụng cấu hình `ci/01-basic.gitlab-ci.yml`. Có ba stage:

```text
build:   build-job
              ↓
test:    test-job1    test-job2 (sleep 20)
              ↓            ↓
deploy:        deploy-prod
```

Hai job test có thể chạy song song nếu runner có đủ khả năng xử lý. Stage deploy đợi cả hai hoàn tất. Job `deploy-prod` chỉ in thông báo và ghi nhận environment `production`, chưa triển khai ứng dụng thật.

## Chạy cấu hình mẫu

1. Tạo dự án GitLab trống rồi đẩy mã nguồn theo README.
2. Vào **Settings → CI/CD → General pipelines → CI/CD configuration file**.
3. Nhập `ci/01-basic.gitlab-ci.yml` và lưu.
4. Vào **Build → Pipelines → New pipeline**, chọn nhánh và chạy.
5. Mở từng job để xem log. `build-job` chào bằng biến `GITLAB_USER_LOGIN`; `deploy-prod` in nhánh từ `CI_COMMIT_BRANCH`.

Có thể thay nội dung `.gitlab-ci.yml` bằng cấu hình mẫu rồi commit nếu muốn thực hiện đúng cách chỉnh file như đề. Chỉ dùng một cách chọn cấu hình tại một thời điểm.

Sau khi lấy minh chứng, đặt đường dẫn cấu hình về `.gitlab-ci.yml` để chạy bản cuối.

## Nếu job bị pending

Kiểm tra runner được bật, tag phù hợp và hạn mức chạy CI còn khả dụng. Runner dùng cho các cấu hình này cần hỗ trợ Docker/container image; shell executor không áp dụng trường `image`.
