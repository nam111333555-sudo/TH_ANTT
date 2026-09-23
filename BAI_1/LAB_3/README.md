# LAB 3 - SecureLogger: Hệ thống ghi nhật ký bảo mật

## Mục tiêu
Xây dựng hệ thống ghi log (`SecureLogger`) tích hợp vào API validate (kế thừa từ [LAB_1](../LAB_1)) với các tính năng:
- Ghi log đa cấp độ (DEBUG, INFO, WARNING, ERROR, CRITICAL) theo định dạng JSON.
- Tự động phát hiện và che (mask) thông tin định danh cá nhân (PII) như email, token/apikey/password trong nội dung log.
- Luân phiên (rotate) log khi vượt quá dung lượng, kèm nén gzip bản log cũ.
- Tạo chữ ký SHA-256 cho từng dòng log (`secure.log.sig`) để phát hiện thay đổi trái phép (tamper detection).

## Cấu trúc
```
BAI_1/LAB_3/
├── app.py                      # Flask API tích hợp validate + secure logging
├── securevalidator/            # Copy từ LAB_1
│   ├── __init__.py
│   └── core.py
├── securelogger/
│   ├── __init__.py
│   └── logger.py               # Core logic: mask PII, rotate log, ký log
├── requirements.txt
└── README.md
```

## Ghi chú sửa lỗi so với tài liệu gốc
Trong `append_signature(line)`, đã bổ sung ký tự xuống dòng `\n` khi ghi hash vào `secure.log.sig`:
```python
f.write(hash_line(line) + "\n")
```
Nếu không có `\n`, các mã hash sẽ bị dính liền nhau trên cùng một dòng, gây khó khăn khi đối chiếu kiểm tra tính toàn vẹn log sau này.

## Cài đặt và chạy

```
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt     # Linux/macOS/Git Bash
.venv\Scripts\pip install -r requirements.txt            # Windows PowerShell/cmd

python app.py
```
Server chạy tại `http://localhost:5000`.

## Kiểm thử qua Postman (hoặc curl)

Gửi `POST` tới `http://localhost:5000/validate` với Body raw JSON:
```json
{
    "email": "phuoc@example.com",
    "url": "https://secure.com",
    "filename": "report.pdf",
    "sql": "OR 1=1 --",
    "html": "<script>alert(1)</script>"
}
```

Tương đương bằng curl:
```
curl -X POST http://localhost:5000/validate -H "Content-Type: application/json" -d "{\"email\":\"phuoc@example.com\",\"url\":\"https://secure.com\",\"filename\":\"report.pdf\",\"sql\":\"OR 1=1 --\",\"html\":\"<script>alert(1)</script>\"}"
```

Kết quả trả về đã sanitize (SQL injection bị lọc, HTML đã escape).

## Kiểm tra nhật ký

- Mở `secure.log`: mỗi dòng là 1 bản ghi JSON, trường `data`/`results` đã che PII, ví dụ `email` chuyển thành `<email_masked>`.
- Mở `secure.log.sig`: mỗi dòng là hash SHA-256 tương ứng với 1 dòng log — dùng để đối chiếu phát hiện log có bị chỉnh sửa trái phép hay không.

> `secure.log`, `secure.log.sig` và các log đã rotate/nén (`*.gz`) không được đưa lên repo (xem `.gitignore`) vì đây là dữ liệu runtime, không phải mã nguồn.
