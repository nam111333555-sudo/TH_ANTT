# LAB 1 - SAST-TOOL (5.2 Thực hành)

Công cụ phân tích bảo mật tĩnh cho Python, phát hiện mẫu mã có rủi ro,
kiểm tra chất lượng mã bằng Flake8 và xuất báo cáo SARIF 2.1.0.

## Cấu trúc

```text
LAB_1/
├── image/                      # 4 ảnh minh chứng
└── sast-tool/
    ├── examples/               # Hai mẫu dễ lỗi và một mẫu an toàn
    ├── rules/                  # Luật và mức độ cảnh báo
    ├── sast_tool/              # Năm thành phần phân tích và CLI
    ├── tests/                  # 14 unittest
    └── requirements.txt
```

## Cài đặt và chạy

```bash
cd sast-tool
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m sast_tool.main examples/vulnerable_01.py -o report-01.sarif
python -m sast_tool.main examples/vulnerable_02.py -o report-02.sarif
python -m sast_tool.main examples/safe_example.py -o report-safe.sarif
```

Cài extension SARIF Viewer của Microsoft trong VS Code và mở tệp `.sarif`
để xem cảnh báo cùng vị trí trong mã nguồn.

## Chức năng

- `ASTAnalyzer`: duyệt AST, tìm lời gọi trực tiếp eval/exec mà không chạy mã.
- `VulnPatternMatcher`: nhận diện mật khẩu gán cố định, import pickle và regex tùy chỉnh.
- `SecurityRuleEngine`: đọc luật JSON và gán mức độ cảnh báo.
- `CodeQualityChecker`: chạy Flake8, xử lý đường dẫn Windows và vị trí dòng/cột.
- `SarifReporter`: xuất JSON SARIF có rule, severity và vị trí nguồn.

## Kết quả

```text
Ran 14 tests in ...
OK
```

![Kiểm thử SAST](image/01_kiem_thu_sast.jpg)

Quét ba mẫu lần lượt cho **5**, **2** và **0** cảnh báo.

![Quét ba tệp mẫu](image/02_ket_qua_quet_sast.jpg)

![SARIF Viewer và vị trí eval](image/03_sarif_viewer.png)

![Danh sách cảnh báo SARIF](image/04_danh_sach_canh_bao_sarif.png)

## Giới hạn

Các chuỗi mật khẩu trong examples chỉ là dữ liệu giả phục vụ bài học.
Import pickle là tín hiệu cần xem xét, chưa chứng minh có khai thác.
Công cụ chưa phân tích taint, alias và shadowing đầy đủ; số cảnh báo Flake8
có thể thay đổi theo phiên bản và cách định dạng mã.
