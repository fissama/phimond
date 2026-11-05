# Triển khai Phimond lên homelab (k3s + Harbor + ArgoCD)

Luồng: push `main` (repo `fissama/phimond`) → GitHub Actions `release-main` → test → tag `vX.Y.Z` → build 2 image lên Harbor →
bump tag trong `fissama/phimond-infra` → ArgoCD (Application `phimond`) rollout vào namespace `phimond` → Traefik → Cloudflare Tunnel.

| Thành phần | Image | Ghi chú |
|---|---|---|
| Server Go | `harbor.philand.io.vn/phimond/phimond-server:vX.Y.Z` | `apps/game-server/Dockerfile`, cổng 8090, **1 bản sao, Recreate** |
| Web (client Vite) | `harbor.philand.io.vn/phimond/phimond-web:vX.Y.Z` | `deploy/web/Dockerfile`, nginx không root, cổng 8080, 2 bản sao |

> **Phimond là hệ thống độc lập**, chỉ dùng chung hạ tầng với philandz trên cùng homelab:
> k3s cluster, ArgoCD instance (ns `argocd`), Harbor instance, MySQL instance, Cloudflare tunnel `philand-01`.
> Ranh giới cô lập: namespace k8s `phimond`, Harbor project `phimond`, database `phimond_reconstruction`,
> user MySQL `phimond`, repo GitOps `fissama/phimond-infra`, host `play.philand.io.vn`.

Một host, cùng origin: `/` → web, `/api` và `/ws` → server. Domain mặc định `play.philand.io.vn`
(đổi trong `server-deployment.yaml` (`GAME_ALLOWED_ORIGINS`, `GAME_PUBLIC_URL`) và `ingress.yaml`).

## Vì sao server chỉ 1 bản sao
Phiên đăng nhập, nhân vật online và giới hạn tốc độ nằm trong bộ nhớ tiến trình. Hai bản sao sẽ lệch trạng thái.
Hệ quả: mỗi lần rollout server **ngắt kết nối người chơi** vài giây, nên workflow bỏ qua thay đổi chỉ về tài liệu/manifest/art nguồn.

## Thiết lập một lần

### Repo GitOps riêng: `fissama/phimond-infra`

Manifest k8s **không** nằm trong repo code. Lý do: repo code có `.git` ~5,8 GB và tree HEAD ~7,1 GB blob
(`apps/game-web/art-src` 3,5 GB / 15.588 file, `apps/game-client` 2,95 GB / 29.549 file).
ArgoCD **không hỗ trợ sparse-checkout** (chỉ CI mới có), nên trỏ thẳng vào repo code sẽ khiến
repo-server phải `git clone --depth 1` ~7 GB và fetch lại mỗi commit.

| Repo | Nội dung | Phạm vi |
|---|---|---|
| `fissama/phimond` | code server + client + `deploy/web` (Dockerfile, nginx.conf) | public |
| `fissama/phimond-infra` | **nguồn chân lý duy nhất** của manifest: `deploy/phimond/*` + `deploy/argocd/phimond.yaml` | public |

ArgoCD đọc repo public → **không cần repo credential** trong ArgoCD.

### Các bước thiết lập

1. **Harbor**: tạo project `phimond` + robot account `phimond-ci` (quyền push + pull, chỉ trong project `phimond`).
   Tên đầy đủ để `docker login` là `robot$phimond+phimond-ci` (Harbor 2.14 gắn tên robot theo `<project>+<robot>`).
   Robot này là credential CI duy nhất của Phimond — không dùng `admin` của Harbor.
   Lưu ý: Harbor **bỏ qua** trường `secret` khi tạo robot qua API → phải `PATCH /api/v2.0/robots/{id}` để set secret sau,
   hoặc lấy secret trả về lúc POST.
2. **GitHub Secrets** của repo `fissama/phimond`: `HARBOR_HOST` (`harbor.philand.io.vn`), `HARBOR_USER` (`robot$phimond+phimond-ci`),
   `HARBOR_PASS` (mật khẩu robot), `INFRA_DEPLOY_KEY` (private key SSH) + `INFRA_KNOWN_HOSTS`.
   Bật branch protection cho `main` (chặn force push).
   - **Deploy key SSH** (không dùng PAT): tạo keypair ed25519, đăng ký public key làm **deploy key (write)** trên `fissama/phimond-infra`,
     rồi lưu private key + `known_hosts` (3 host key của github.com, lấy từ `GET /meta`) vào 2 secret trên.
     Blast radius đúng 1 repo; không cần copy/paste token cá nhân, không lộ quyền repo khác.
     Workflow clone bằng `git@github.com:${INFRA_REPO}.git` với `GIT_SSH_COMMAND` trỏ vào `~/.ssh/id_deploy`.
   - Harbor robot đặt tên đầy đủ theo Harbor 2.14: `robot$<project>+<robot>` (ở đây `robot$phimond+phimond-ci`).
3. **Repo `fissama/phimond-infra`**: **nguồn chân lý duy nhất** của manifest k8s — `deploy/phimond/*.yaml`,
   `deploy/phimond/jobs/migrate-job.yaml`, `deploy/argocd/phimond.yaml`.
   Manifest **không** nằm trong repo code (thư mục `deploy/homelab/` đã dọn khỏi `fissama/phimond`).
   Mọi thay đổi hạ tầng của Phimond đều commit ở repo này, không đụng `philandz/infra`.
4. **Namespace riêng `phimond`**: cần Secret `harbor-pull` trong namespace này (SealedSecret như `philandz/infra`'s
   `deploy/bootstrap/`, tạo lại cho namespace `phimond`) và Secret `phimond-env`.
5. **Secret `phimond-env`**: tạo bằng `kubeseal` (cert công khai lấy từ `kube-system/sealed-secrets-key*`), commit SealedSecret
   vào `phimond-infra/deploy/phimond/sealed-env.yaml`. Không commit giá trị thật. Dùng **database MỚI**
   (`phimond_reconstruction`) và user chỉ có quyền trên database đó.
   - `MYSQL_HOST=192.168.1.11` — IP LAN của homelab (MySQL container `philand.mysql` publish `0.0.0.0:3306`).
     ⚠️ IP này do DHCP cấp, có thể đổi. Nếu DB lại hỏng, kiểm tra `ip -4 addr show wlp1s0` trên homelab rồi cập nhật secret.
   - `MYSQL_TLS=false` — MySQL 8.4.7 có `require_secure_transport=OFF`.
6. **GAME_TRUSTED_PROXIES**: mặc định `10.42.0.0/16` (dải pod k3s). Traefik pod IP `10.42.0.4` → nằm trong dải này, giữ nguyên.
   Xác minh bằng `kubectl -n kube-system get pods -o wide | grep traefik`.
7. **Cloudflare Tunnel** (dùng chung tunnel `philand-01`): thêm vào `/etc/cloudflared/config.yml` trên homelab
   ```
   - hostname: play.philand.io.vn
     service: http://127.0.0.1:30958     # cùng upstream Traefik như v2.philand.io.vn
   ```
   rồi `sudo systemctl restart cloudflared`. Cần SSH vào `philand-01` (chạy `cloudflared access login` trước nếu bị `bad handshake`).
   Cập nhật cả bản mirror `philandz/scripts/cloudflared_config.yml` trong repo `philandz/infra`.
   Tạo bản ghi DNS `play.philand.io.vn` trỏ về Cloudflare (các host hiện có dùng A record proxy).
8. Áp Application: `ssh philand-01 'sudo k3s kubectl apply -f phimond.yaml'` (file từ `phimond-infra/deploy/argocd/`).

## Lần phát hành đầu (v1.0.0)
1. Bảo đảm commit đầu của `main` là commit đã kiểm tra, rồi `git push origin main`. Workflow chạy test, tạo tag `v1.0.0` (khi chưa có tag nào),
   build và push image, bump infra.
2. **Trước khi server khởi động lần đầu: tạo database và chạy migration** (không hoàn tác được):
   - Dump nếu database đã tồn tại: `mysqldump --single-transaction phimond_reconstruction > phimond-YYYYMMDD.sql`.
   - `kubectl apply -f deploy/phimond/jobs/migrate-job.yaml` rồi `kubectl -n phimond logs -f job/phimond-migrate`.
     Binary `-migrate` tự tạo database riêng và áp 001, 002, 003 theo thứ tự. Migration 003 chưa từng chạy trên MySQL thật,
     theo dõi log kỹ.
   - Pod server chưa Ready đến khi database có đủ bảng; cứ chạy migrate trước rồi `kubectl -n phimond rollout restart deploy/phimond-server`.
3. ArgoCD sync tự động. Kiểm tra: `kubectl -n phimond get pods`, `kubectl -n phimond logs deploy/phimond-server`.

## Phát hành các bản sau
Push `main` với commit `<type>(<scope>): <subject>` (feat|fix|docs|style|refactor|perf|test|chore|ci|build|deploy|art).
Version: có `!` hoặc `BREAKING CHANGE` → major, có `feat` → minor, còn lại → patch (tính trên mọi commit từ tag trước).
Có migration mới: dump, xóa job cũ (`kubectl -n phimond delete job phimond-migrate`), chạy lại job, rồi để server rollout.

## Kiểm tra sau deploy
- `curl -s https://play.philand.io.vn/healthz` (web nginx) → `ok`.
- `curl -s https://play.philand.io.vn/api/content | head -c 200` → JSON (server).
- Mở game, đăng ký tài khoản thử, tạo nhân vật, vào game, rồi xóa tài khoản thử bằng chức năng xóa tài khoản của game.
- Mở `/hd2d/assets.json`, một vài PNG (`/hd2d/walker-boy.run.png`) không 404.
- **Để yên trong game 2–3 phút** xem WebSocket có bị rớt không (xem Rủi ro).

## Quay lại bản cũ
- Đổi tag image về bản trước trong `fissama/phimond-infra` (`git revert` commit `chore(deploy): update phimond ...`); ArgoCD tự rollout.
- Database chỉ đi tiến: quay lại image cũ không hoàn tác migration. Muốn hoàn tác dữ liệu phải khôi phục từ dump.

## Rủi ro đã biết
1. **WebSocket và Cloudflare**: Cloudflare ngắt kết nối WebSocket im lặng sau khoảng 100 giây. Server và client hiện **không có ping/heartbeat**
   (chưa xác minh game có gửi dữ liệu định kỳ khi đứng yên). Nếu bị rớt, cần thêm ping 30 giây ở server hoặc client (thay đổi mã, cần phát hành riêng).
2. **Kích thước repo**: `.git` ~5,8 GB, tree HEAD ~7,1 GB blob (49.079 file; `apps/game-web/art-src` 3,5 GB và `apps/game-client` 2,95 GB).
   Workflow dùng `sparse-checkout` + `filter: blob:none` (chỉ lấy `apps/game-server`, `apps/client`, `packages`, `data`, `migrations`, `deploy`) để CI không tải art nguồn.
   ArgoCD **không** có sparse-checkout → manifest phải nằm ở repo riêng `fissama/phimond-infra` (đã tách), nếu không ArgoCD sẽ clone ~7 GB.
   Nếu thêm thư mục mới mà Dockerfile cần, phải thêm vào `sparse-checkout`.
3. **IP homelab do DHCP**: `MYSQL_HOST` đang trỏ `192.168.1.11` (IP LAN của node k3s). Mất điện hoặc hết hạn DHCP là IP đổi →
   server không kết nối được MySQL. Khi đó: `ip -4 addr show wlp1s0` trên homelab, rồi `kubectl -n phimond rollout restart deploy/phimond-server`
   sau khi cập nhật `MYSQL_HOST` trong SealedSecret `phimond-env`.
4. **Image chưa được build thử cục bộ** (không có Docker trong môi trường phát triển). Lần chạy CI đầu là lần build thật đầu tiên.
5. **Dockerfile.dockerignore** riêng cho web và server; `.dockerignore` gốc của Godot cũ không bị thay đổi.
6. Server Go chưa từng build/test đầy đủ ngoài máy chủ có mạng (module `golang.org/x/crypto`, `filippo.io/edwards25519`); `go test ./...` trong CI là cổng kiểm tra đầu tiên.
7. **Đây là hệ thống độc lập**: mọi thay đổi trong `phimond-infra` chỉ ảnh hưởng namespace `phimond`. Không được đụng service của philandz
   (`philandz`, `philand`, `philand-sandbox` namespace) hay repo `philandz/infra`.
