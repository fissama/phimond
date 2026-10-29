-- Nhiều nhân vật mỗi tài khoản (3 ô). Nhân vật cũ giữ ô 0 và id bằng id tài khoản.
ALTER TABLE characters ADD COLUMN slot TINYINT UNSIGNED NOT NULL DEFAULT 0 AFTER account_id;
ALTER TABLE characters ADD UNIQUE KEY uq_characters_slot (account_id, slot);
ALTER TABLE characters DROP INDEX account_id;
ALTER TABLE sessions ADD COLUMN character_id CHAR(32) NULL;
