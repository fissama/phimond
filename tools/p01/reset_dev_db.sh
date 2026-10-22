#!/bin/sh
# Xóa toàn bộ dữ liệu người chơi trong DB DEV để chơi lại từ đầu với 5 map Đợt A (P01 §9 D3).
# Sao lưu (mysqldump, nén gzip) vào _backup/ TRƯỚC khi xóa. Giữ nguyên schema và schema_migrations.
#
#   sh tools/p01/reset_dev_db.sh            # chỉ in kế hoạch, không xóa
#   sh tools/p01/reset_dev_db.sh --yes      # sao lưu rồi xóa
#
# Cần mysql + mysqldump (macOS: brew install mysql-client) và file .env ở gốc repo với
# MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, GAME_DB_NAME (MYSQL_TLS=true nếu dùng TLS).
# Chỉ chạy với DB có tên chứa "phimond" và KHÔNG chứa "prod".
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$root"
[ -f .env ] || { echo "Thiếu .env ở gốc repo" >&2; exit 1; }
set -a
# shellcheck disable=SC1091
. ./.env
set +a
DB=${GAME_DB_NAME:-${MYSQL_DATABASE:-}}
case "$DB" in
  *prod*|"") echo "Từ chối: tên DB '$DB' rỗng hoặc giống production" >&2; exit 1 ;;
  *phimond*) ;;
  *) echo "Từ chối: tên DB '$DB' không chứa 'phimond'" >&2; exit 1 ;;
esac
TABLES="pet_ancestry pets audit_events command_receipts sessions characters accounts"
SSL=""
[ "${MYSQL_TLS:-}" = "true" ] && SSL="--ssl-mode=REQUIRED"
CNF=$(mktemp)
trap 'rm -f "$CNF"' EXIT
chmod 600 "$CNF"
printf '[client]\nhost=%s\nport=%s\nuser=%s\npassword=%s\n' "$MYSQL_HOST" "${MYSQL_PORT:-3306}" "$MYSQL_USER" "$MYSQL_PASSWORD" > "$CNF"

echo "DB: $DB @ $MYSQL_HOST"
for t in $TABLES; do
  n=$(mysql --defaults-extra-file="$CNF" $SSL -N -e "SELECT COUNT(*) FROM \`$DB\`.\`$t\`" 2>/dev/null || echo "?")
  echo "  $t: $n dòng"
done
if [ "${1:-}" != "--yes" ]; then
  echo "Chưa xóa gì. Chạy lại với --yes để sao lưu rồi xóa."
  exit 0
fi
mkdir -p _backup
OUT="_backup/${DB}-$(date +%Y%m%d-%H%M%S).sql.gz"
mysqldump --defaults-extra-file="$CNF" $SSL --single-transaction --no-tablespaces --set-gtid-purged=OFF "$DB" $TABLES | gzip > "$OUT"
[ -s "$OUT" ] || { echo "Sao lưu rỗng, dừng" >&2; exit 1; }
echo "Đã sao lưu: $OUT"
SQL="SET FOREIGN_KEY_CHECKS=0;"
for t in $TABLES; do SQL="$SQL DELETE FROM \`$DB\`.\`$t\`;"; done
SQL="$SQL SET FOREIGN_KEY_CHECKS=1;"
mysql --defaults-extra-file="$CNF" $SSL -e "$SQL"
echo "Đã xóa dữ liệu người chơi. Khôi phục nếu cần: gunzip -c $OUT | mysql ... $DB"
