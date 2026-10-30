# Tài khoản người chơi

## Chính sách hiện hành (v1.0.1)

- Tên đăng nhập 3–24 ký tự `[A-Za-z0-9_]`, không phân biệt hoa/thường (cột MySQL `ascii_general_ci`).
- Mật khẩu 8–72 byte. Bị từ chối: nằm trong danh sách mật khẩu phổ biến (`persistence/account.go`), lặp một ký tự, trùng tên đăng nhập. Không bắt buộc chữ hoa/số/ký tự đặc biệt.
- Đăng nhập không áp lại chính sách độ dài: tài khoản cũ (≥10 ký tự) vẫn vào được.
- Lỗi trả về có `code` ổn định + `message` tiếng Việt: `username_format`, `password_short|long|weak`, `username_taken`, `credentials`, `email_invalid|taken`, `terms_required`, `rate_limited`, `reset_invalid`, `session`.
- Đăng ký bắt buộc `terms: true` (hộp đồng ý Điều khoản + Chính sách; trang tĩnh `/terms.html`, `/privacy.html`).
- Email tuỳ chọn: nhập khi đăng ký hoặc thêm/đổi/gỡ ở Menu → Cài đặt → Tài khoản.
- Quên mật khẩu: `POST /api/password/forgot {email}` luôn trả 200; nếu có tài khoản thì gửi thư chứa liên kết `…/#reset=<64 hex>` hiệu lực 30 phút, dùng một lần. Đặt lại thành công thu hồi mọi phiên.
- Xoá tài khoản: `POST /api/account/delete {password}`; xoá vĩnh viễn tài khoản, mọi nhân vật, linh thú, nhật ký, phiên.
- Phiên 7 ngày; client nhớ token (localStorage, hoặc sessionStorage nếu bỏ chọn "Ghi nhớ") và vào lại đúng nhân vật sau khi tải lại.

## Cấu hình máy chủ (biến môi trường)

| Biến | Ý nghĩa |
|---|---|
| `GAME_TRUSTED_PROXIES` | Danh sách CIDR/IP (phẩy) của reverse proxy tin cậy, ví dụ `127.0.0.1,172.16.0.0/12`. Chỉ khi kết nối đến từ các địa chỉ này mới tin `X-Forwarded-For`. **Đặt khi chạy sau nginx/Caddy**, nếu không mọi người chơi dùng chung một bộ đếm giới hạn tần suất theo IP của proxy. |
| `GAME_PUBLIC_URL` | URL công khai của game, dùng tạo liên kết trong thư đặt lại mật khẩu (`https://phimond.example`). |
| `GAME_SMTP_ADDR`, `GAME_SMTP_USER`, `GAME_SMTP_PASS`, `GAME_MAIL_FROM` | SMTP gửi thư. Thiếu `GAME_SMTP_ADDR` thì chỉ ghi log (kể cả mã đặt lại): **không dùng ở production**. |

Proxy phải ghi đè (không nối thêm) `X-Forwarded-For` bằng IP thật của khách, ví dụ nginx `proxy_set_header X-Forwarded-For $remote_addr;`.

## Migration

`migrations/003_account_recovery.sql` thêm cột `accounts.email` (UNIQUE) và bảng `password_resets`. Chạy bằng bộ migrate hiện có khi khởi động. **Chưa kiểm trên MySQL thật**: các test Go dùng kho trong bộ nhớ; hãy chạy thử đăng ký → thêm email → quên mật khẩu → xoá tài khoản trên bản staging có MySQL trước khi mở.

## Việc cần chủ dự án / tư vấn pháp lý quyết định (Việt Nam)

Đây là ghi chú kỹ thuật, không phải tư vấn pháp lý.

1. **Xác thực danh tính người chơi.** Quy định về dịch vụ trò chơi điện tử trên mạng (Nghị định 147/2024/NĐ-CP và văn bản sửa đổi) có yêu cầu thu thập/xác thực thông tin người chơi (họ tên, ngày sinh, số điện thoại…) đối với trò chơi có tương tác. Bản này **chưa** thu các thông tin đó. Cần xác nhận game thuộc loại nào và có buộc phải xác thực không.
2. **Giấy phép.** Trò chơi điện tử G1 (có tương tác giữa người chơi với nhau và với hệ thống) cần giấy phép/đăng ký theo luật; chưa xử lý.
3. **Dưới 16 tuổi.** Cần cơ chế cha mẹ/người giám hộ đăng ký nếu cho phép; hiện chỉ nêu trong Điều khoản.
4. **Dữ liệu cá nhân.** Nghị định 13/2023/NĐ-CP (bảo vệ dữ liệu cá nhân) yêu cầu thông báo mục đích xử lý, đồng ý, quyền truy cập/xoá; trang `/privacy.html` là bản nháp có chỗ [điền] đơn vị vận hành, nơi đặt máy chủ, nhà cung cấp SMTP, thời gian lưu nhật ký.
5. **Đơn vị vận hành.** Cần tên pháp nhân/cá nhân và email hỗ trợ thật điền vào hai trang pháp lý.
