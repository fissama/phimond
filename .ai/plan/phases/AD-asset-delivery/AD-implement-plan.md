# AD — Tải asset cho client web: kế hoạch triển khai

- **Ngày:** 2026-11-18. **Trạng thái:** DRAFT, chờ owner duyệt §8.
- **Vấn đề owner báo:** v1.1.0 kéo rất nhiều ảnh về trình duyệt (tab Network dày request), gây chậm, rò tài nguyên và các lỗi kèm theo.
- **Liên quan:** nợ P01 **N08** (R08 tải/giải phóng theo map, budget, `?bench=`) và **N07** (Low phải nhẹ hơn High). Phase này trả một phần hai nợ đó.
- **Phạm vi:** `apps/client` (render, loader, UI skin), `tools/` dựng asset, `deploy/web/nginx.conf`, `.github/workflows/release-main.yml`, một kho lưu (S3/R2) + CDN. Không đổi server Go, giao thức, save người chơi.

## 1. Hiện trạng (đối chiếu code 2026-11-18, chưa đo trên trình duyệt)

| # | Phát hiện | Bằng chứng | Hệ quả |
|---|---|---|---|
| F1 | 830 file lẻ trong `apps/client/public` (78 MB): 781 PNG, 32 WebP. `hd2d/` 453 file (34 MB), `ui/` 13 MB, `battle/` 7,2 MB, `pets/` 14 MB, `audio/` 11 MB | `find public` | Mỗi prop/decal/icon/nút = 1 request. Một map nhiều kit = hàng trăm request |
| F2 | Ảnh **không băm tên**, nginx cho `max-age=3600`; `.json` là `no-cache` | `deploy/web/nginx.conf` dòng 25–34 | Sau 1 giờ mỗi lần vào lại game, trình duyệt hỏi lại **từng ảnh** (304). Đây là nguồn chính của "rất nhiều request" khi chơi lại |
| F3 | Texture PNG giải nén thành RGBA; cache texture budget cố định **160 MB**, chỉ đẩy ra khi vượt budget; không đổi theo preset Low/Medium/High | `src/render/assets.ts` `TextureCache` | Bộ nhớ GPU giữ ở mức cao suốt phiên; iPhone Safari dễ giật/tải lại tab; Low không nhẹ hơn High (N07) |
| F4 | **Rò texture thật:** nền xa dùng `textures.get(...).clone()` nhưng `disposables` chỉ có `geo, mat`, không có `tex` | `src/render/scene.ts` khoảng dòng 838–850 | Mỗi lần vào map có nền xa tạo một texture không bao giờ dispose; source ảnh gốc bị giữ dù cache đã đẩy ra. Tăng dần theo số lần đổi map |
| F5 | UI dựng bằng CSS `background-image` cho từng nút/khung (9-slice), icon, chữ số sát thương từng ảnh | `src/ui/skin.ts` (`nine()`, `damageGlyphs`) | Mở menu/trận đấu bắn thêm hàng chục request nhỏ |
| F6 | Prefetch map kề chỉ lấy ảnh nền (`backdrop`), không lấy prop/sàn | `src/game/world.ts` `prefetchNeighbors` | Qua cổng vẫn phải tải phần lớn ảnh map mới, màn tải lâu |
| F7 | File nặng không cần thiết: `victory.wav` 2,1 MB (WAV không nén), nhạc OGG/MP3 1,3–2,9 MB, nền trận PNG 1,2–1,7 MB | `find -size +300k` | Tải lần đầu nặng |
| F8 | Toàn bộ 78 MB nằm trong image Docker `phimond-web` | `deploy/web/Dockerfile` | Đổi một ảnh phải build + rollout cả image (ngắt người chơi); homelab gánh hết băng thông |
| F9 | Ảnh ở đường dẫn công khai, tên dễ đoán (`/hd2d/bush-01.png`) | `hd2dUrl()` | Ai cũng tải được toàn bộ art bằng script |

Giả định cần đo xác nhận ở AD0: số request lần đầu/lần sau, dung lượng, thời gian đổi map, bộ nhớ GPU sau nhiều vòng đổi map.

## 2. Mục tiêu (đề xuất, owner chốt ở §8)

| Chỉ số | Hiện tại | Mục tiêu đề xuất |
|---|---|---|
| Request ảnh khi **vào lại** game (cache còn) | hàng trăm (304) | **≤ 5** (chỉ manifest) |
| Request ảnh khi vào một map lần đầu | đo ở AD0 | giảm ≥ 70% |
| Dung lượng tải lần đầu tới khi chơi được (Triệu Linh Điện) | đo ở AD0 | giảm ≥ 40% |
| Bộ nhớ texture GPU ước tính (Low / Medium / High) | ≤ 160 MB mọi preset | ≤ 64 / 96 / 160 MB |
| Bộ nhớ sau 10 vòng đổi map | tăng dần (F4) | **phẳng** (dao động ≤ 10%) |
| Thời gian đổi map sang map kề đã prefetch | đo ở AD0 | ≤ 500 ms desktop, ≤ 1,5 s iPhone |
| Hiển thị | — | ảnh chụp 11 map trước/sau **không khác pixel** (trừ chỗ đã duyệt đổi định dạng) |

## 3. Các hướng đã cân nhắc (debate)

| Hướng | Được | Mất | Kết luận |
|---|---|---|---|
| Để Vite tự băm (`import.meta.glob` toàn bộ ảnh) | Băm tên miễn phí, ít code | Vite xử lý 78 MB mỗi build; khó tách sang CDN; manifest asset do script Python sinh vẫn phải nối với tên băm | **Không chọn.** Dùng bước dựng riêng sinh manifest băm, dùng chung cho nginx và CDN |
| Bước dựng riêng `tools/assets/build_runtime.py` | Một nguồn sự thật: băm, atlas, đổi định dạng, manifest; chạy được trong CI | Thêm một script phải bảo trì | **Chọn** |
| Atlas toàn game | Ít request nhất | Tải cả thứ chưa cần; đổi 1 prop phải dựng lại tất cả | **Không chọn** |
| Atlas theo **kit/map** (prop, decal, NPC, icon UI) | Giảm mạnh request, ít đổi texture khi vẽ | Phải sửa loader dùng UV; cần chừa viền chống lem pixel | **Chọn**; sàn lặp (`repeat`) và nền xa giữ ảnh riêng vì cần wrap |
| WebP/AVIF | Nhẹ hơn 30–70% dung lượng tải | Không giảm bộ nhớ GPU | **Chọn WebP** (lossless cho pixel art/UI, lossy cho nền trận/nền xa); AVIF để sau vì mã hoá chậm |
| KTX2/Basis (nén GPU) | Bộ nhớ GPU giảm 4–8 lần | Thêm bộ giải mã ~200 KB; có thể nhoè pixel art | **Hoãn**, chỉ làm nếu đo iPhone vẫn vượt budget sau AD2+AD3; nếu làm chỉ áp cho sàn/nền lớn |
| S3/CDN cho asset chạy thật | Image web nhẹ, đổi art không cần rollout, homelab hết gánh băng thông | Thêm dịch vụ ngoài, CORS, khóa CI, chi phí | **Chọn** ở AD6, sau khi băm tên (không băm thì CDN cache sai) |
| Service Worker | Vào lại gần như 0 request, offline một phần | Dễ kẹt bản cũ nếu sai | **Tùy chọn** sau AD6; băm tên + cache 1 năm đã đạt gần như cùng hiệu quả |
| Chặn lấy art | — | Không có cách chặn tuyệt đối ảnh trình duyệt đã hiển thị | Chỉ tăng độ khó (AD7); không hứa "bảo vệ" |

## 4. Các bước

Mỗi bước một nhóm commit nhỏ. Commit đổi `apps/client`/`deploy` sẽ ra bản patch; gộp bước để giảm số lần rollout (§6).

### AD0 — Đo trước (baseline) + `?bench=` (trả một phần N08)
- Thêm chế độ `?bench=1` trong client: overlay nhỏ hiển thị `textures.stats()`, `renderer.info.memory` (textures/geometries), số request ảnh từ `performance.getEntriesByType('resource')`, thời gian tải map (`__phimondLastMapLoadMs` đã có), FPS trung bình.
- Script Playwright `apps/client/tests/e2e/bench.spec.ts`: vào game → đi vòng Triệu Linh Điện → Bìa Rừng → Rừng Sâu → Hoàng Môn → Quảng Trường → Thương Phố, lặp 10 vòng; ghi JSON: request lần đầu/lần hai, byte, thời gian đổi map, bộ nhớ sau mỗi vòng. Chạy 3 preset.
- Lưu kết quả `.ai/plan/phases/AD-asset-delivery/evidence/baseline-<ngày>.json` + bảng tóm tắt.
- Đo tay trên iPhone Safari thật (owner), ghi vào cùng file.
- **Xong khi:** có số baseline cho mọi dòng ở §2.

### AD1 — Băm tên + cache dài + dọn file nặng
- `tools/assets/build_runtime.py`: đọc `apps/client/public/{hd2d,ui,battle,pets,audio}` (đầu ra hiện tại của `tools/p01/sync_client_assets.py`), ghi `build/runtime-assets/<nhóm>/<tên>.<hash8>.<ext>` + `asset-manifest.json` (`"hd2d/bush-01.png" → "hd2d/bush-01.3fa9c1d2.png"`, kèm kích thước, byte). Hash = SHA-256 nội dung. Chạy lại không đổi gì nếu ảnh không đổi.
- Client: một hàm `assetUrl(logicalPath)` tra manifest (nạp 1 lần lúc khởi động, có fallback về tên cũ khi thiếu). Thay `hd2dUrl`, `uiUrl`, `petUrl`, nhạc, ảnh trận, CSS skin dùng hàm này.
- nginx: file có hash → `Cache-Control: public, max-age=31536000, immutable`; `asset-manifest.json` → `no-cache` (nhỏ, có ETag); bỏ `max-age=3600` cho ảnh.
- Audio: `victory.wav` → OGG/MP3; nhạc nền giữ bitrate hợp lý (đề xuất 96–128 kbps), nhạc map chỉ tải khi vào map đó (kiểm tra `music.ts`).
- Dockerfile: bước build chạy `build_runtime.py` (cần Python + Pillow trong stage build, hoặc chạy trong CI trước `docker build` rồi copy).
- Test: unit cho `assetUrl` (có/thiếu manifest); validator: mọi id trong `assets.json`/`ui.json` có trong manifest; e2e: lần tải thứ hai **không** có request ảnh nào trả 304/200 từ mạng (chỉ từ cache).
- **Xong khi:** vào lại game ≤ 5 request ảnh; ảnh chụp 11 map không đổi.

### AD2 — Sửa rò và budget theo preset (trả N07 + một phần N08)
- Sửa F4: đưa texture `clone()` của nền xa vào `disposables`; rà toàn bộ `clone()`, `new THREE.Texture`, `CanvasTexture`, material tạo động trong `render/` (`scene.ts`, `atmosphere.ts`, `engine.ts`, sprite người chơi/NPC/quái, hiệu ứng trận) xem có dispose khi rời map/trận không.
- `TextureCache`: budget theo preset (Low 64 / Medium 96 / High 160 MB, chỉnh theo số đo); khi đổi map: bỏ pin tất cả, **pin lại chỉ texture của map mới + map kề**, đẩy phần còn lại ngay (không chờ vượt budget). Texture đã đẩy vẫn còn trong cache HTTP nên quay lại nhanh.
- Low: giảm kích thước nền xa/nền trận (bản 50% sinh ở AD1), tắt texture trang trí phụ (decal nhiều lớp), giới hạn pixel ratio.
- Kiểm tra rò ở trận đấu: vào/ra trận 20 lần, `renderer.info.memory.textures` không tăng.
- Test e2e: 10 vòng đổi map + 20 lần vào/ra trận, bộ nhớ phẳng; Low đo nhỏ hơn High (đóng N07 khi có số).
- **Xong khi:** đạt dòng "bộ nhớ" và "sau 10 vòng" ở §2 trên Chromium; iPhone đo tay.

### AD3 — Atlas theo kit/map + UI sprite sheet
- `build_runtime.py` thêm bước gói atlas (thuật toán MaxRects, viết bằng Python + Pillow, không thêm công cụ ngoài): nhóm theo kit (`town`, `forest`, `hall`, `palace`, `farm`, `arena`…) hoặc theo danh sách prop từng map (`MAP_PROPS/MAP_EXTRAS/MAP_DECALS`); trang tối đa 2048×2048 (an toàn cho iPhone), **viền 2 px kéo dài mép (extrude)** chống lem khi lọc, giữ pixel nguyên (không co giãn).
- Manifest atlas: mỗi id có `atlas`, `rect [x,y,w,h]`, giữ `px`, `pivot_px`, `frames`. Ảnh có nhiều khung (idle/run) xếp liền trong cùng atlas.
- Không gói: sàn lặp (`repeat`), nền xa, nền trận, ảnh pet lớn (đã là atlas P10).
- Client: sprite/prop dùng chung texture atlas, mỗi mesh có UV riêng (sửa `PlaneGeometry` UV hoặc `texture.offset/repeat` trên bản clone chia sẻ source; chọn UV hình học để không nhân texture). Cập nhật `TextureCache` đếm byte theo trang atlas.
- UI: gói icon, chữ số sát thương, nút trạng thái nhỏ thành 1–3 sprite sheet, CSS dùng `background-position`; khung 9-slice lớn giữ ảnh riêng (9-slice với sprite sheet dễ lỗi).
- Test: validator atlas (mọi id có rect, không chồng nhau, nằm trong trang, viền đúng); so ảnh chụp 11 map + HUD + menu + trận trước/sau, sai khác pixel = 0 (ngoài vùng đã duyệt).
- **Xong khi:** request ảnh khi vào map lần đầu giảm ≥ 70% so với baseline.

### AD4 — Định dạng nhẹ hơn
- Prop/UI/sprite: **WebP lossless** (hoặc PNG đã tối ưu bằng `oxipng`/Pillow `optimize` nếu WebP lossless không nhỏ hơn); chọn theo file nào nhỏ hơn, ghi vào manifest.
- Nền trận, nền xa: **WebP lossy** chất lượng ~85, owner duyệt bằng mắt từng ảnh (bảng so sánh trong `evidence/`).
- Giữ PNG gốc trong `art/`; chỉ bản chạy thật đổi định dạng.
- Safari iOS 14+ đọc WebP; ghi rõ phiên bản tối thiểu.
- **Xong khi:** đạt dòng "dung lượng tải lần đầu" ở §2.

### AD5 — Thứ tự tải và prefetch
- Chia tài nguyên map thành **thiết yếu** (sàn, người chơi, NPC, cổng, va chạm hiển thị) và **trang trí** (prop xa, decal, động vật, hiệu ứng). Tắt màn tải khi xong phần thiết yếu; phần trang trí hiện dần (fade 150 ms).
- Prefetch map kề: lấy **toàn bộ** atlas + sàn + nền của map kề (không chỉ nền), chạy lúc rảnh (`requestIdleCallback`), giới hạn 4 request song song, không prefetch khi `navigator.connection.saveData` hoặc mạng chậm, không prefetch ở preset Low trên di động (tùy số đo).
- **Xong khi:** đạt dòng "đổi map sang map kề" ở §2.

### AD6 — Kho lưu S3/R2 + CDN
- Kho: **Cloudflare R2** (không tính phí băng thông ra, có CDN và custom domain) — đề xuất; phương án khác: AWS S3 + CloudFront (phí băng thông), MinIO trên homelab (không giảm tải homelab). Owner chốt §8.
- Bucket `phimond-assets` (public đọc qua CDN, ví dụ `cdn.philand.io.vn`): chỉ chứa **bản chạy thật đã băm** (vài chục MB). CORS cho `play.philand.io.vn` (Three.js cần để dùng ảnh khác domain làm texture). Chặn liệt kê thư mục.
- CI (`release-main.yml`): sau test, chạy `build_runtime.py` → upload file mới lên bucket (file có hash không bao giờ ghi đè) → upload `asset-manifest.json` theo version (`manifest/v1.1.3.json`) → build image web. Khóa bucket trong GitHub Secrets (quyền chỉ ghi vào bucket này). **Không xoá** file cũ ngay: giữ ít nhất 3 bản phát hành gần nhất để người đang chơi bản cũ không vỡ ảnh.
- Client: biến `VITE_ASSET_BASE` (mặc định cùng origin). Giai đoạn 1: image web **vẫn chứa** asset làm đường dự phòng (lỗi CDN → thử lại cùng origin). Giai đoạn 2 (sau ≥ 2 tuần ổn định): bỏ asset khỏi image, image chỉ còn JS/HTML.
- Đổi art sau AD6: chỉ cần dựng + upload + đổi manifest; vẫn đi qua CI để có kiểm tra, nhưng có thể làm workflow riêng `assets-publish.yml` không rollout pod (owner chốt).
- **Riêng (không thuộc CDN):** bucket **private** `phimond-art-backup` để backup `art/` (~11 GB ảnh trung gian chỉ có trên máy owner) bằng `rclone sync` chạy từ Mac. Thay cho bản `art-backup-20261116/` đang cùng ổ đĩa.
- **Xong khi:** game chạy với ảnh từ CDN; tắt CDN thử thì fallback hoạt động; image web giảm dung lượng (giai đoạn 2).

### AD7 — Giảm việc lấy art (tùy chọn, làm cùng AD3/AD6)
- Tên băm + atlas: không còn đường dẫn dễ đoán từng prop.
- CDN: chặn hotlink theo Referer (chỉ cho `play.philand.io.vn`), giới hạn tốc độ theo IP, tắt liệt kê.
- Không đưa ảnh chưa phát hành vào bucket/manifest (chỉ asset `approved` của bản đang chạy).
- Ghi rõ giới hạn: người đã vào game vẫn lấy được ảnh từ bộ nhớ trình duyệt; đây chỉ là tăng độ khó.

### AD8 — Service Worker (tùy chọn, sau AD6)
- Precache manifest + atlas của map đang ở và map kề; cache-first cho file có hash; network-first cho `asset-manifest.json`, `index.html`. Xoá cache bản cũ khi manifest đổi.
- Chỉ làm nếu số đo AD6 vẫn thấy request lặp đáng kể.

## 5. Kiểm thử chung (mọi bước)

- `cd apps/client && npm run check` (typecheck, unit, build) và `npm run e2e` (Chromium; WebKit khi có, nợ N11).
- `python3 tools/p01/build_maps.py --check`; validator asset mới (`build_runtime.py --check`): manifest đủ id, hash đúng nội dung, atlas không chồng.
- So ảnh chụp: 11 map × 3 preset + HUD + menu + 1 trận, trước/sau. Lưu `evidence/screens-<bước>/`.
- Bench AD0 chạy lại sau mỗi bước, so với baseline; ghi vào `evidence/`.
- iPhone Safari thật: owner đo tay sau AD2, AD3, AD6.

## 6. Phát hành (gộp để giảm số lần ngắt người chơi)

| Bản | Gồm | Loại commit | Ghi chú |
|---|---|---|---|
| v1.1.1 | AD0 + AD1 + AD2 | `perf:`/`fix:` (patch) | Lợi ích lớn nhất, rủi ro thấp. Sửa rò F4 |
| v1.1.2 | AD3 + AD4 + AD5 | `perf:` | Đổi loader/UV: cần so ảnh kỹ |
| v1.1.3 | AD6 (giai đoạn 1) + AD7 | `feat:` nếu thêm cấu hình CDN → **minor** (v1.2.0); owner chọn | Cần tài khoản R2/S3 + DNS |
| sau | AD6 giai đoạn 2, AD8 | `perf:` | Khi đã ổn định |

Trước mỗi push: liệt kê thay đổi, chạy đủ §5; push khi owner ra lệnh. Commit chỉ đổi tài liệu/`tools/` không ra bản (paths-ignore).

## 7. Rủi ro

- **Người đang chơi giữ `index.html` cũ** khi bản mới ra: tên băm cũ phải còn trên server/CDN ít nhất vài bản phát hành (AD6 không xoá file cũ ngay; giai đoạn image còn chứa asset thì bản cũ nằm trong image cũ đã bị thay — chấp nhận người chơi tải lại trang).
- **Lem pixel ở mép atlas**: bắt buộc extrude viền + Nearest filter + so ảnh pixel.
- **Sai pivot/UV** làm prop lệch chân: validator so `pivot_px` trước/sau, ảnh chụp map.
- **CDN lỗi/khóa CI lộ**: fallback cùng origin; khóa chỉ quyền ghi một bucket; xoay khóa định kỳ.
- **WebP lossy làm hỏng nét pixel art**: chỉ áp cho nền trận/nền xa, owner duyệt bằng mắt.
- **Môi trường build**: Docker stage build cần Python + Pillow (hoặc chạy trong CI rồi copy). Không cài gì thêm trên máy owner ngoài thứ đã có; Mac VM có Python + Pillow.
- **Tăng độ phức tạp loader** ảnh hưởng P19/P02 (icon item, trận 1v3): AD1 đưa mọi đường dẫn qua `assetUrl()` sớm để phase sau dùng chung.

## 8. Cần owner chốt

1. **Mục tiêu số ở §2** có ổn không (đặc biệt budget Low/Medium/High và thời gian đổi map trên iPhone)?
2. **Kho lưu**: Cloudflare R2 (đề xuất), AWS S3 + CloudFront, hay MinIO trên homelab? Domain CDN dùng gì (`cdn.philand.io.vn`)? DNS `philand.io.vn` đang ở đâu (nếu ở Cloudflare thì R2 gắn domain nhanh nhất)?
3. **Có làm bucket backup `art/` (private) không**, dùng cùng nhà cung cấp?
4. **Mức chống lấy art** (AD7): chỉ tên băm + chặn hotlink, hay cần hơn (watermark ảnh gốc)?
5. **Gộp phát hành** như §6 hay tách nhỏ hơn? AD6 tính `feat` (lên v1.2.0) hay `perf` (v1.1.3)?
6. **Làm AD trước P19** (đề xuất: ít nhất v1.1.1 trước, vì P19 thêm icon item sẽ dùng `assetUrl()`), hay chạy song song?
