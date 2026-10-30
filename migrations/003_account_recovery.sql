-- Email tuỳ chọn để khôi phục mật khẩu; mã đặt lại mật khẩu dùng một lần (chỉ lưu băm).
ALTER TABLE accounts ADD COLUMN email VARCHAR(254) CHARACTER SET ascii COLLATE ascii_general_ci NULL AFTER password_hash;
ALTER TABLE accounts ADD UNIQUE KEY uq_accounts_email (email);
CREATE TABLE IF NOT EXISTS password_resets (
 token_hash BINARY(32) PRIMARY KEY,
 account_id CHAR(32) NOT NULL,
 expires_at DATETIME(6) NOT NULL,
 FOREIGN KEY (account_id) REFERENCES accounts(id),
 INDEX (expires_at)
) ENGINE=InnoDB;
