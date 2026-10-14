# LAB 1 - Web Vulnerability Scanner (4.2 Thực hành: WebVulnScanner)

Công cụ quét minh họa các rủi ro phổ biến của ứng dụng web: XSS, SQL Injection, CSRF và SSRF. Kết quả quét được tổng hợp thành báo cáo và có giao diện Flask để lựa chọn loại kiểm tra.

## Cấu trúc

```text
LAB_1/
├── image/                  # Ảnh minh chứng thực hiện Lab 1
└── web-vuln-scanner/
    ├── scanners/           # XSSScanner, SQLInjectionTester, CSRFDetector, SSRFTester
    ├── report/             # Tạo báo cáo lỗ hổng
    ├── tests/              # 9 unittest
    ├── ui/                 # Flask app và HTML templates
    ├── main.py             # Chương trình minh họa trên terminal
    └── requirements.txt
```

## Cài đặt và chạy

```bash
cd web-vuln-scanner
pip install -r requirements.txt

python -m unittest discover -s tests -v
python main.py
python ui/app.py
```

Sau khi chạy giao diện, mở `http://127.0.0.1:5000` trên trình duyệt.

## Chức năng

- `XSSScanner`: gửi các payload XSS mẫu và kiểm tra payload có bị phản chiếu trong phản hồi HTTP hay không.
- `SQLInjectionTester`: kiểm tra các payload SQL Injection trong tham số của URL.
- `CSRFDetector`: kiểm tra sự xuất hiện của các tên CSRF token phổ biến trong HTML.
- `SSRFTester`: phát hiện các địa chỉ nội bộ như `127.0.0.1`, `localhost`, dải `10.x.x.x`, `192.168.x.x` và `172.16.x.x` đến `172.31.x.x`.
- `ReportGenerator`: hợp nhất các kết quả để hiển thị trong báo cáo.

## Kết quả kiểm thử

```text
Ran 9 tests in ...
OK
```

Ảnh trong thư mục `image/` ghi lại việc cài đặt thư viện, chạy 9 unittest, chạy chương trình chính, khởi động giao diện Flask, quét SQL Injection/CSRF/SSRF và demo XSS cục bộ.

## Giới hạn của bản minh họa

- SQL Injection và SSRF hiện kiểm tra chuỗi payload trong URL, chưa xác minh khai thác trên máy chủ đích.
- CSRF trên giao diện sử dụng HTML mô phỏng.
- Việc payload XSS xuất hiện trong phản hồi là tín hiệu cần xem xét, chưa đủ để khẳng định JavaScript có thể thực thi trong mọi ngữ cảnh.
