# Triển khai Phimond lên homelab (k3s + Harbor + ArgoCD)

Luồng: push `main` (repo `fissama/phimond`) → GitHub Actions `release-main` → test → tag `vX.Y.Z` → build 2 image lên Harbor →
bump tag trong `philandz/infra` → ArgoCD (Application `phimond`) rollout vào namespace `phimond` → Traefik → Cloudflare Tunnel.

| Thành phần | Image | Ghi chú |
|---|---|---|
| Server Go | `harbor.philand.io.vn/philand/phimond-server:vX.Y.Z` | `apps/game-server/Dockerfile`, cổng 8090, **1 bản sao, Recreate** |
| Web (client Vite) | `harbor.philand.io.vn/philand/phimond-web:vX.Y.Z` | `deploy/web/Dockerfile`, nginx không root, cổng 8080, 2 bản sao |

Một host, cùng origin: `/` → web, `/api` và `/ws` → server. Domain mặc định `play.philand.io.vn`
(đổi trong `server-deployment.yaml` (`GAME_ALLOWED_ORIGINS`, `GAME_PUBLIC_URL`) và `ingress.yaml`).

## Vì sao server chỉ 1 bản sao
Phiên đăng nhập, nhân vật online và giới hạn tốc độ nằm trong bộ nhớ tiến trình. Hai bản sao sẽ lệch trạng thái.
Hệ quả: mỗi lần rollout server **ngắt kết nối người chơi** vài giây, nên workflow bỏ qua thay đổi chỉ về tài liệu/manifest/art nguồn.

## Thiết lập một lần
1. **Harbor**: project `philand` đã có. Bảo đảm user CI có quyền push `phimond-server` và `phimond-web`.
2. **GitHub Secrets** của repo `fissama/phimond`: `HARBOR_HOST`, `HARBOR_USER`, `HARBOR_PASS`, `GH_REPO_PAT`
   (PAT đọc và push `philandz/infra`). Bật branch protection cho `main` (chặn force push).
3. **Repo `philandz/infra`**: chép `deploy/homelab/phimond/*.yaml` (không chép thư mục `secrets/`) vào `deploy/phimond/`,
   và `deploy/homelab/phimond/jobs/` vào `deploy/phimond/jobs/`. Chép `deploy/homelab/argocd/phimond.yaml` vào `deploy/argocd/`
   (so với `gateway.yaml` để khớp repoURL, project).
4. **Namespace riêng `phimond`**: cần Secret `harbor-pull` trong namespace này (SealedSecret như `deploy/bootstrap/`, tạo lại cho
   namespace `phimond`) và Secret `phimond-env`.
5. **Secret `phimond-env`**: tạo từ `secrets/phimond-env.secret.example.yaml` (điền thật), mã hóa bằng `kubeseal`
   rồi commit SealedSecret vào `infra/deploy/phimond/sealed-secret.yaml`. Không commit giá trị thật. Dùng **database MỚI**
   (mặc định `phimond_reconstruction`) và user chỉ có quyền trên database đó.
6. **GAME_TRUSTED_PROXIES**: mặc định `10.42.0.0/16` (dải pod mặc định k3s). Xác minh bằng
   `kubectl -n kube-system get pods -o wide | grep traefik`, đặt dải chứa IP của Traefik. Sai giá trị thì giới hạn tốc độ nhìn mọi
   người chơi là cùng một IP.
7. **Cloudflare Tunnel**: thêm vào `/root/.cloudflared/config.yml` trên homelab
   ```
   - hostname: play.philand.io.vn
     service: http://127.0.0.1:30958     # cùng upstream Traefik như v2.philand.io.vn
   ```
   rồi `sudo systemctl restart cloudflared`. Cần SSH vào `philand-01` (chạy `cloudflared access login` trước nếu bị `bad handshake`).
8. Áp Application: `ssh philand-01 'sudo k3s kubectl apply -f phimond.yaml'`.

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
- Đổi tag image về bản trước trong `philandz/infra` (`git revert` commit `chore(deploy): update phimond ...`); ArgoCD tự rollout.
- Database chỉ đi tiến: quay lại image cũ không hoàn tác migration. Muốn hoàn tác dữ liệu phải khôi phục từ dump.

## Rủi ro đã biết
1. **WebSocket và Cloudflare**: Cloudflare ngắt kết nối WebSocket im lặng sau khoảng 100 giây. Server và client hiện **không có ping/heartbeat**
   (chưa xác minh game có gửi dữ liệu định kỳ khi đứng yên). Nếu bị rớt, cần thêm ping 30 giây ở server hoặc client (thay đổi mã, cần phát hành riêng).
2. **Kích thước repo**: `.git` ~5,8 GB và ~15.600 file `apps/game-web/art-src` đang được git theo dõi. Workflow dùng `sparse-checkout` + `filter: blob:none`
   (chỉ lấy `apps/game-server`, `apps/client`, `packages`, `data`, `migrations`, `deploy`) để CI không tải art nguồn. Clone mới trên máy khác vẫn rất nặng;
   về lâu dài nên đưa `art-src` ra khỏi repo (Git LFS hoặc repo riêng). Nếu thêm thư mục mới mà Dockerfile cần, phải thêm vào `sparse-checkout`.
3. **Image chưa được build thử cục bộ** (không có Docker trong môi trường phát triển). Lần chạy CI đầu là lần build thật đầu tiên.
4. **Dockerfile.dockerignore** riêng cho web và server; `.dockerignore` gốc của Godot cũ không bị thay đổi.
5. Server Go chưa từng build/test đầy đủ ngoài máy chủ có mạng (module `golang.org/x/crypto`, `filippo.io/edwards25519`); `go test ./...` trong CI là cổng kiểm tra đầu tiên.
