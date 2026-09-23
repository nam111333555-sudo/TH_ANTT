import unittest
from securevalidator import (
    validate_email, validate_url, validate_filename,
    sanitize_sql_input, sanitize_html_input
)

class TestAdvancedBypasses(unittest.TestCase):
    def setUp(self):
        print("\n Running:", self._testMethodName)

    def test_validate_email_internal_routing(self):
        # Định dạng (Format) hợp lệ theo Regex, nhưng nếu server dùng email này để phân giải DNS nội bộ,
        # hacker có thể kích hoạt lỗi SSRF (Giả mạo yêu cầu từ máy chủ) qua server mail.
        self.assertTrue(validate_email("admin@127.0.0.1"))

    def test_validate_url_decimal_ip_bypass(self):
        # Kỹ thuật dùng IP dạng Thập phân (Decimal IP). 
        # Số 2130706433 chính là 127.0.0.1, hoàn toàn qua mặt được danh sách đen (Blacklist) dạng chuỗi.
        self.assertTrue(validate_url("http://2130706433/admin/delete"))
        
    def test_validate_url_short_ip_bypass(self):
        # Kỹ thuật dùng IP viết tắt (Short IP). 127.1 sẽ được trình duyệt/mạng tự hiểu là 127.0.0.1
        self.assertTrue(validate_url("http://127.1/admin"))

    def test_validate_filename_windows_dos(self):
        # Kỹ thuật dùng tên tệp tin dành riêng (Reserved filenames) của Windows như CON, PRN, LPT1.
        # Nếu server là Windows, việc thao tác với file tên "CON" sẽ làm treo ứng dụng, gây ra lỗi từ chối dịch vụ (DoS).
        self.assertTrue(validate_filename("CON"))

    def test_sanitize_sql_input_unicode_normalization(self):
        # Kỹ thuật chuẩn hóa Unicode (Unicode Normalization). 
        # Trong Python, \w mặc định khớp với cả các ký tự Unicode dạng Fullwidth. 
        # Khi chuỗi này vào Database, DB có thể tự chuyển đổi nó thành chữ cái bình thường và thực thi lệnh.
        input_str = "ＳＥＬＥＣＴ" # Đây là chữ S-E-L-E-C-T dạng Fullwidth
        sanitized = sanitize_sql_input(input_str)
        self.assertEqual(sanitized, "ＳＥＬＥＣＴ") # Vượt qua \w trót lọt

    def test_sanitize_html_input_javascript_uri(self):
        # Kỹ thuật khai thác qua giao thức mạng (URI Scheme payload).
        # Hàm html.escape() vô dụng nếu kết quả này được đặt vào thuộc tính <a href="Giá_trị_nhập_vào">
        input_str = "javascript:alert(1)"
        sanitized = sanitize_html_input(input_str)
        # Các ký tự chữ và số không bị mã hóa, XSS (Mã độc xuyên trang) vẫn xảy ra khi người dùng click vào link.
        self.assertEqual(sanitized, "javascript:alert(1)")