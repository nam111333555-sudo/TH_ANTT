# BÁO CÁO THỰC HÀNH BÀI 6

**Chủ đề:** Bảo mật với DevSecOps — GitLab CI/CD và Docusaurus

**Ngày thực hiện:** 28/10/2026

**Họ tên / MSSV / Lớp:** ........................................................

## 1. Mục tiêu và môi trường

Thực hiện mục 6.2.1 và 6.2.2 của tài liệu `lab-06 (1).pdf`: tạo pipeline cơ bản,
build Docusaurus, truyền artifacts và triển khai website lên GitLab Pages.
Phân tích các biện pháp bảo mật pipeline theo phần 6.1.

Môi trường cục bộ: Windows, PowerShell, Node.js 24.14.0, npm 11.9.0,
Docusaurus 3.10.2. Pipeline cơ bản dùng Alpine 3.22; pipeline website dùng
image `node:24-bookworm-slim` trên GitLab runner.

- [Repository thực hành GitLab](https://gitlab.com/hutech-group7321144/lab-06-devsecops)
- [Website GitLab Pages](https://lab-06-devsecops-58b0f2.gitlab.io/)
- [Repository nộp bài GitHub](https://github.com/nam111333555-sudo/TH_ANTT)

## 2. Cơ sở lý thuyết: bảo mật CI/CD (6.1)

DevSecOps tích hợp bảo mật trong quá trình phát triển và triển khai, giúp phát
hiện lỗi sớm và hạn chế đưa cấu hình hoặc thư viện không an toàn vào hệ thống.

| Thành phần | Biện pháp |
|---|---|
| Kiểm soát truy cập | MFA, phân quyền tối thiểu, bảo vệ nhánh và review thay đổi pipeline |
| Quản lý secrets | Dùng biến CI/CD hoặc vault, không commit token/mật khẩu |
| Tính toàn vẹn | Lockfile, npm ci, chữ ký commit và artifact khi được cấu hình |
| Security gates | Kiểm tra bắt buộc trước deploy; job lỗi phải chặn giai đoạn sau |
| Audit | Lưu log job và artifacts, theo dõi thay đổi cấu hình |
| Runner | Cô lập môi trường, cập nhật và hạn chế quyền truy cập |

SAST phân tích mã nguồn; DAST kiểm thử ứng dụng đang chạy; SCA kiểm tra
dependency; secret scanning phát hiện khóa bị lộ; IaC scanning kiểm tra cấu hình
hạ tầng trước triển khai. Các loại kiểm tra này có phạm vi khác nhau và cần
đánh giá kết quả theo ngữ cảnh.

## 3. LAB_1: pipeline cơ bản (6.2.1)

Pipeline có ba stage `build → test → deploy`. Build in lời chào bằng
`GITLAB_USER_LOGIN`; hai test có thể chạy song song; test-job2 chờ 20 giây;
deploy-prod in tên nhánh bằng `CI_COMMIT_BRANCH`.

Pipeline **#2997167768** đạt Passed, có bốn job thành công. Deploy trong Lab 1
chỉ mô phỏng bằng echo, chưa phát hành website.

![Hình 1. Pipeline cơ bản thành công](LAB_1/image/01_pipeline_co_ban.png)

![Hình 2. Build job in lời chào](LAB_1/image/02_build_job.png)

![Hình 3. Test job chờ 20 giây](LAB_1/image/03_test_job2.png)

![Hình 4. Deploy mô phỏng trên main](LAB_1/image/04_deploy_prod.png)

## 4. LAB_2: Docusaurus và GitLab Pages (6.2.2)

Đầu tiên tạo job in `This is my first job!` và chạy `date`. Tiếp theo thêm
mã nguồn Docusaurus, dùng `npm ci` và `npm run build` để tạo website tĩnh.
Thư mục build được lưu trong artifacts để job sau sử dụng.

Pipeline build **#2997188462** thành công. Artifact có `index.html`, `assets/`,
`docs/`, `404.html` và `sitemap.xml`.

![Hình 5. Job đầu tiên và ngày giờ](LAB_2/image/05_job_dau_tien.png)

![Hình 6. Build Docusaurus và lưu artifact](LAB_2/image/06_build_docusaurus.png)

![Hình 7. Nội dung artifact](LAB_2/image/07_artifact_build.png)

Pipeline triển khai **#2997205623**, commit `b15f728`, có hai stage build và
deploy. Các job `build-job`, `pages`, `pages:deploy` đều thành công. Job Pages
tải artifact, đổi `build/` thành `public/` và phát hành website.

![Hình 8. Pipeline build/deploy thành công](LAB_2/image/08_pipeline_build_deploy.png)

![Hình 9. Log job Pages](LAB_2/image/09_pages_job.png)

![Hình 10. Pages Active và URL website](LAB_2/image/10_pages_url.png)

![Hình 11. Website Docusaurus trên GitLab Pages](LAB_2/image/11_website_docusaurus.png)

## 5. Kết quả kiểm tra và đánh giá bảo mật

- Năm kiểm thử URL triển khai tại máy đều thành công; bao gồm localhost,
  đường dẫn dự án, unique domain, biến URL ghi đè và giao thức không hợp lệ.
- Build cục bộ thành công; trang chủ, năm trang tài liệu, CSS và JS trả HTTP 200.
- Đã xử lý phát hiện HIGH/CRITICAL trong dependency gián tiếp bằng overrides
  `tinypool@2.1.2` và `serialize-javascript@7.1.3`, sau đó kiểm tra lại build.
- Audit sau bản vá: 0 HIGH/CRITICAL, còn 3 LOW và 17 MODERATE tính theo package
  bị ảnh hưởng; log npm ci trên GitLab cũng ghi nhận 20 package bị ảnh hưởng.
- `npm audit --omit=dev --audit-level=high` tại máy trả exit code 0.

Pipeline minh chứng hai stage chưa chạy Trivy, SAST hoặc DAST. Các bản mở rộng
được cung cấp trong mã nguồn để thực hành thêm; chưa có bằng chứng MFA,
vault, bảo vệ nhánh hoặc ký số đã được bật trên GitLab.

## 6. Kết luận

Đã thực hiện pipeline cơ bản, build và truyền artifacts, triển khai Docusaurus
lên GitLab Pages. Website hiển thị trên unique domain; ảnh thực tế ghi nhận các
job thành công và deployment Active. Các cảnh báo dependency LOW/MODERATE
còn lại cần được theo dõi khi tiếp tục phát triển.
