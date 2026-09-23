# LAB 2 - GitSecure: Pre-commit Hook bảo mật

## Mục tiêu
Xây dựng git hook `pre-commit` tên **GitSecure** để tự động quét mã nguồn trước khi commit, nhằm ngăn chặn:
- Bí mật bị mã hóa cứng (API key, token, mật khẩu...)
- Tệp có quyền ghi công khai (world-writable, trên Unix/Linux)
- Lỗ hổng bảo mật cơ bản trong mã Python (quét tĩnh bằng `bandit`)

Mọi phát hiện được ghi vào `gitsecure.log` (không đưa lên repo) và nếu có vi phạm, commit sẽ bị chặn (`exit(1)`).

## Cấu trúc
```
BAI_1/LAB_2/
├── .githooks/
│   └── pre-commit          # Script hook chính (Python)
├── .venv/                  # Môi trường ảo chứa bandit (không đưa lên repo)
├── requirements.txt         # bandit
└── README.md
```

## Cài đặt

1. Tạo virtual environment và cài bandit:
   ```
   python -m venv BAI_1/LAB_2/.venv
   BAI_1/LAB_2/.venv/bin/python -m pip install -r BAI_1/LAB_2/requirements.txt
   ```

2. Trỏ Git đến thư mục hook:
   ```
   git config core.hooksPath BAI_1/LAB_2/.githooks
   ```

3. Cấp quyền thực thi cho script (Git Bash / Unix):
   ```
   chmod +x BAI_1/LAB_2/.githooks/pre-commit
   ```

## Kiểm thử

Tạo file vi phạm chứa mật khẩu cứng (thay `<TU_KHOA>` bằng `password` và giá trị bất kỳ trên 4 ký tự để tự thử):
```
mkdir BAI_1/LAB_2/pre-commit-hook-test
printf '%s = "%s"\n' <TU_KHOA> 123456 > BAI_1/LAB_2/pre-commit-hook-test/bad.py
git add BAI_1/LAB_2/pre-commit-hook-test/bad.py
git commit -m "test"
```

Kết quả mong đợi: commit bị chặn với thông báo `COMMIT BLOCKED by GitSecure!` và chi tiết được ghi vào `gitsecure.log`.

Sau khi kiểm thử, xóa file/thư mục vi phạm và commit lại — hook sẽ in `GitSecure: All checks passed!` và cho phép commit tiếp tục.

## Ghi chú
- Trên Windows, việc kiểm tra quyền tệp (`world-writable`) được bỏ qua (`platform.system() == "Windows"`) vì mô hình quyền tệp khác Unix.
- `bandit` được gọi từ `.venv` cục bộ của LAB_2 (không có sẵn `bandit` toàn cục trong PATH trên môi trường Windows/MSYS2 dùng ở đây); nếu không tìm thấy, hook sẽ tự dùng `bandit` trong PATH hệ thống.
