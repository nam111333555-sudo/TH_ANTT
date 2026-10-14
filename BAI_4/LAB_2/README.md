# LAB 2 - JWT Security Tools (4.4 Thực hành: JWTSecure)

Bộ công cụ minh họa kiểm tra JWT, thử khóa bí mật yếu theo wordlist, quản lý access/refresh token, tạo URL OAuth 2.0 và bảo vệ endpoint Flask bằng JWT.

## Cấu trúc

```text
LAB_2/
├── image/                     # Ảnh minh chứng thực hiện Lab 2
└── jwt-security-tools/
    ├── api_gateway/           # Flask API bảo vệ endpoint /protected
    ├── jwt_cracker/           # Thử secret JWT theo wordlist
    ├── jwt_validator/         # Kiểm tra tính hợp lệ của token
    ├── oauth_client/          # Tạo authorization URL, đổi code lấy token
    ├── token_manager/         # Tạo và làm mới token
    ├── tests/                 # 7 pytest
    ├── main.py                # Tạo token và chạy API
    ├── pytest.ini
    └── requirements.txt
```

## Cài đặt và chạy

```bash
cd jwt-security-tools
pip install -r requirements.txt

python -m pytest tests/ -v
python main.py
```

`main.py` in access token, refresh token và chạy API tại `http://127.0.0.1:5000`.

Mở terminal khác để gọi endpoint với access token vừa tạo:

```bash
curl -i -H "Authorization: Bearer <access_token>" http://127.0.0.1:5000/protected
```

Kết quả token hợp lệ:

```json
{"message":"Access granted","user":"AN"}
```

Token sai phải trả về HTTP `401`:

```json
{"message":"Access denied"}
```

## Chức năng

- `JWTValidator`: xác thực chữ ký và thời hạn JWT.
- `JWTCracker`: thử secret trong wordlist bằng nhiều luồng xử lý.
- `OAuthClient`: tạo authorization URL và gửi authorization code để nhận token.
- `TokenManager`: tạo access token, refresh token và tạo access token mới từ refresh token.
- `APIGateway`: kiểm tra JWT trong header `Authorization: Bearer <token>` trước khi cho phép truy cập `/protected`.

## Kết quả kiểm thử

```text
7 passed
```

Ảnh trong thư mục `image/` ghi lại kết quả pytest, gọi API bằng token hợp lệ với người dùng `AN`, và trường hợp token không hợp lệ trả về `401`.

## Lưu ý

Các secret trong source là dữ liệu mô phỏng phục vụ Lab. Khi phát triển ứng dụng thực tế, cần dùng secret đủ mạnh, lưu bằng biến môi trường hoặc secret manager, và kiểm tra token `type` để chỉ access token được phép truy cập API.
