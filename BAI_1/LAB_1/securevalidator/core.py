import re, html, urllib.parse, os

def validate_email(email: str) -> bool:
    """Validate email format (Kiểm tra định dạng email)."""
    # Dùng Regex (Biểu thức chính quy) chuẩn và chặt chẽ hơn
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.fullmatch(pattern, email) is not None

def validate_url(url: str) -> bool:
    """Validate URL and prevent basic SSRF vectors (Kiểm tra URL và ngăn chặn các hướng tấn công giả mạo yêu cầu máy chủ cơ bản)."""
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ['http', 'https'] or not parsed.netloc:
            return False
            
        # Chặn các IP nội bộ / Localhost (Private IPs / Localhost)
        hostname = parsed.hostname.lower() if parsed.hostname else ""
        if hostname in ['localhost', '127.0.0.1', '::1'] or hostname.startswith('192.168.'):
            return False
            
        return True
    except Exception:
        return False

def validate_filename(filename: str) -> bool:
    """Prevent path traversal attacks (Ngăn chặn tấn công duyệt qua thư mục)."""
    # Bổ sung chặn Null byte injection (Chèn byte rỗng)
    if '\0' in filename or ".." in filename or "/" in filename or "\\" in filename:
        return False
    return os.path.basename(filename) == filename

def sanitize_sql_input(input_str: str) -> str:
    """
    Sanitize SQL input (Làm sạch đầu vào SQL).
    LƯU Ý: Chỉ áp dụng hàm này cho Column/Table names (Tên cột/bảng).
    """
    # Sử dụng Whitelist (Danh sách trắng) thay vì Blacklist. Chỉ cho phép chữ, số và dấu gạch dưới.
    sanitized = re.sub(r"[^\w]", "", input_str)
    return sanitized.strip()

def sanitize_html_input(html_str: str) -> str:
    """Escape HTML input to prevent XSS (Mã hóa đầu vào HTML để ngăn chặn tấn công mã độc xuyên trang)."""
    # quote=True đảm bảo mã hóa cả dấu nháy đơn và kép (' và ")
    return html.escape(html_str, quote=True)