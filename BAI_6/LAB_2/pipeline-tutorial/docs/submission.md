---
title: Minh chứng và nộp bài
sidebar_position: 5
---

# Checklist nộp bài

Báo cáo, README từng lab và ảnh thực tế nằm trong thư mục `BAI_6` của repository nộp bài. Điền thông tin cá nhân vào báo cáo trước khi nộp.

- [ ] Họ tên, MSSV, lớp, URL repository, URL Pages.
- [ ] Ảnh pipeline cơ bản gồm `build-job`, `test-job1`, `test-job2`, `deploy-prod`.
- [ ] Log `build-job` có lời chào và log `test-job2` có bước chờ 20 giây.
- [ ] Log job đầu tiên có thông báo và ngày giờ.
- [ ] Log build Docusaurus thành công, artifact có `build/index.html`.
- [ ] Ảnh pipeline hai stage build/deploy theo mục 6.2.2.
- [ ] Log job Pages và URL trong Deploy → Pages.
- [ ] Ảnh website Docusaurus trên URL Pages, CSS và điều hướng hoạt động.
- [ ] Giải thích stage, job, image, script, artifacts và security gates.

Nếu chạy bản mở rộng, đính kèm kết quả scan thực tế và cách xử lý phát hiện. Không ghi “không có lỗ hổng” nếu chưa chạy scanner hoặc scanner không tải được dữ liệu.

Ảnh chụp, URL triển khai và thời gian chạy GitLab lấy từ dự án thực hành. Pipeline minh chứng đã chạy hai stage build/deploy; các bản mở rộng có kiểm thử và scanner được cung cấp riêng để thực hành thêm.
