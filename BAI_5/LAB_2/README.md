# LAB 2 - DAST-TOOL (5.4 Thực hành)

Bộ công cụ giám sát động gồm thống kê tiến trình, kiểm tra bộ nhớ, bộ đếm mạng,
quan sát sự kiện audit, chạy demo trong thư mục tạm và API Flask.

## Cấu trúc

```text
LAB_2/
├── image/                          # 9 ảnh minh chứng
└── dast-tool/
    ├── runtime_monitor.py
    ├── memory_analyzer.py
    ├── network_traffic_analyzer.py
    ├── security_behavior_checker.py
    ├── virtual_sandbox.py
    ├── audit_demo.py
    ├── app.py                      # Năm API Flask
    ├── main.py                     # Chạy minh họa trên terminal
    ├── tests/                      # 16 unittest
    └── requirements.txt
```

## Cài đặt và chạy

```bash
cd dast-tool
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python main.py
python app.py
```

API chạy tại `http://127.0.0.1:5000`. Mở PowerShell khác để kiểm tra:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/monitor | ConvertTo-Json -Depth 6
Invoke-RestMethod http://127.0.0.1:5000/api/memory | ConvertTo-Json -Depth 6
Invoke-RestMethod http://127.0.0.1:5000/api/network | ConvertTo-Json -Depth 6
Invoke-RestMethod http://127.0.0.1:5000/api/security | ConvertTo-Json -Depth 6
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/sandbox -ContentType "application/json" -Body '{"command":"echo Hello Sandbox"}' | ConvertTo-Json -Depth 6
```

## Chức năng

- `RuntimeMonitor`: CPU %, bộ nhớ RSS và tệp mở của một tiến trình.
- `MemoryAnalyzer`: đối tượng GC chưa thu hồi và kiểm tra miền signed 64-bit.
- `NetworkTrafficAnalyzer`: bộ đếm gửi/nhận theo card mạng.
- `SecurityBehaviorChecker`: nhận diện mẫu lời gọi và phân loại sự kiện audit.
- `VirtualSandbox`: lệnh tin cậy trong thư mục tạm, timeout, cleanup; có backend Docker tùy chọn.
- `audit_demo`: ghi nhận sự kiện compile/exec từ chương trình cố định trong Python con.

## Kết quả

```text
Ran 16 tests in ...
OK
```

![Kiểm thử DAST và API](image/01_kiem_thu_dast.png)

![Thông tin tiến trình và bộ nhớ](image/02_chay_dast_tien_trinh_bo_nho.png)

![Audit và demo sandbox](image/03_chay_dast_audit_sandbox.png)

![Khởi động Flask](image/04_khoi_dong_flask.png)

![API monitor](image/05_api_monitor.png)

![API memory](image/06_api_memory.png)

![API network](image/07_api_network.png)

![API security](image/08_api_security.png)

![API sandbox](image/09_api_sandbox.png)

## Giới hạn

Thư mục làm việc tạm không phải cách ly hệ điều hành: backend process chỉ chạy
lệnh tin cậy. API chỉ cho phép echo và bind localhost. Backend Docker bổ sung
giới hạn tài nguyên/quyền và tắt mạng, nhưng chưa được kiểm chứng trong lần chạy này.
GC không phát hiện mọi memory leak; Python int không tự tràn ở 64 bit.
Thống kê mạng là toàn máy, không phải phân tích gói tin hay phát hiện C2.
Sự kiện exec trong demo là tín hiệu cần xem xét ngữ cảnh, không kết luận có mã độc.
