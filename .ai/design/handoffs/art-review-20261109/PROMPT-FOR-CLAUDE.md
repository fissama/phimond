# Prompt bàn giao cho Claude — nghiệm thu art và roadmap toàn bộ 92 map

Bạn tiếp nhận toàn bộ art workstream Phimond từ session Codex. Workspace: `/Users/phileanh/rust/phimond`.

Mục tiêu của tôi: art assets để dựng map HD-2D theo Octopath Traveler, giữ chủng loại vật thể, landmark và bảng màu nhận diện từ map game gốc. Hãy nghiệm thu bằng mắt, quyết định chính xác asset nào duyệt/giữ, sửa đóng gói hay vẽ lại, rồi lập roadmap thực thi đến đủ art của **92 map / 21 kit** theo plan ban đầu. Hãy làm trọn cuộc audit và viết đủ roadmap; không chỉ trả lời bằng nhận xét chung hoặc danh sách tên kit. Phạm vi lần này là nghiệm thu và lập kế hoạch; artwork mới sẽ theo các task/prompt cụ thể bạn chốt.

## 1. Đọc nguồn và xác lập phạm vi

Đọc `AGENTS.md`, `/Users/phileanh/.codex/RTK.md` và các skill phù hợp đang có, ưu tiên `generate2dmap`, `generate2dsprite`, `generate2dmedia` nếu cần xem pipeline. Lệnh shell dùng `rtk`/`rtk proxy`.

Nguồn gốc yêu cầu:

- `.ai/design/hd2d-maps-75-gemini-prompt.md`: plan 75 map còn lại / 17 kit, cộng 17 map đã có art = 92 map / 21 kit. Tên Gemini ở tài liệu là lịch sử; không lấy route Gemini thay cho route hiện được owner yêu cầu.
- `.ai/design/map-checklists/README.md` và toàn bộ `kit-*.md`: checklist từng kit/map, ảnh nguồn, landmark, NPC/dependencies, cổng và asset dùng chung.
- `.ai/design/gpt-redo/00-master-v2.md`: style DNA và quy trình GPT redraw hiện hành.
- `.ai/design/map-checklists/REVIEW-20261029.md`: review Claude trước đây.
- `.ai/design/gpt-redo/PROGRESS.md`: nhật ký thực hiện, gồm candidate, rejected attempts, giới hạn QA và các gói phụ.
- `.ai/design/map-checklists/REDRAW-QUEUE-20261024.md` và `.ai/design/gpt-redo/README.md`: nguồn lịch sử; nhiều số liệu đã cũ, phải đối chiếu file thực tế.
- Ảnh map: `.ai/design/map-checklists/refs/`; bản đầy đủ ở `/Users/phileanh/Downloads/Phimond-P12-Review/map-images/` khi tồn tại.

Không chạy lại generator checklist vì sẽ ghi đè chỉnh tay. Khi tài liệu mâu thuẫn, ghi rõ khác biệt và dùng manifest/file hiện hành cùng bằng chứng review mới nhất để đối chiếu; cờ `approved` chỉ là trạng thái đã ghi, không chứng minh một file mới thay đã được duyệt.

## 2. Gói bàn giao và cách đọc inventory

Đọc trước `.ai/design/handoffs/art-review-20261109/INVENTORY-SUMMARY.md`.

Trong cùng thư mục có:

- `asset-inventory.csv`: từng ID, manifest, file, category, cờ duyệt/status, kích thước thật, hash khai báo/thực tế, raw khai báo, đường dẫn QA/review. Có **1.712 bản ghi trong 39 manifest**, bao gồm baseline, predecessor, redo và auxiliary; **không phải 1.712 asset duy nhất, không phải tất cả đều do phiên chat gần nhất vẽ**.
- `manifest-summary.json`: số bản ghi và cờ duyệt theo từng gói, cùng trạng thái cấp manifest.
- `map-roster.json`: đối chiếu đủ **92 map / 21 kit**.
- `checklist-rows.csv`: giữ nguyên các dòng checklist, kể cả reused/tick cũ; tick Vẽ không tự chứng minh có asset hoặc đã duyệt.
- `raw-artwork-index.csv`: đường dẫn raw và các bản final trước đây trong workspace, kể cả archive/study.
- `session-generated-image-index.csv`: index PNG gốc của thư mục ImageGen session, không copy/đổi tên artwork.
- `raw-provenance-findings.json`: một số workspace raw đã bị PNG re-encode khi lưu. Pixel giải mã giống nhau nhưng byte/hash khác bản ImageGen gốc; vì vậy tuyên bố byte-identical trước đây không đúng cho những file được chỉ ra. Original vẫn còn ở đường dẫn ghi trong JSON và được copy byte-identical vào `generated-originals/` trong gói handoff.
- `git-head.txt`, `git-art-status.txt`: checkpoint nguồn và working tree; có nhiều thay đổi chưa commit từ nhiều công việc, không revert/dọn hàng loạt.
- `world-tree-repeat-corrections/`: preview lặp **3×1 thật** cho edge-03 studies 11, 13–16 và ảnh tổng hợp. Các `repeat-3x.png` cũ trong những study này thực chất chỉ phóng lớn một tile 3 lần, nên không phải bằng chứng repeat hợp lệ. Hãy dùng ảnh sửa đúng này và tự kiểm lại preview các job khác.

Snapshot phát hiện **30 bản ghi lệch SHA256** và **2 bản ghi thiếu manifest.file** (hai bát thức ăn/nước trong P01 predecessor D; file vật lý có). Điều tra từng dòng; đây là phát hiện metadata, chưa phải kết luận phải vẽ lại. Đặc biệt hash `world_tree_gate-landmark-01` trong manifest bị cũ sau sửa lề canvas; file/QA mới cần đối chiếu lại. Không chỉ sửa hash hàng loạt để che một file thay chưa được duyệt.

## 3. Các gói cần bàn giao/nghiệm thu

Chín kit batch-11 hiện có **626 primary manifest records**, tất cả 0 cờ duyệt:

| Kit | Map | Candidate records |
|---|---:|---:|
| desert | 6 | 98 |
| windrock | 6 | 82 |
| nightmare | 6 | 67 |
| tomb | 9 | 76 |
| crossroads | 6 | 62 |
| astral | 7 | 59 |
| ancient | 6 | 55 |
| ghost_castle | 3 | 50 |
| world_tree | 3 | 51 |

Root là `art/src/hd2d/batch-11-<kit>/`: xem manifest, contact sheet, từng final/raw/prompt/review/qa và các preview. Auxiliary gồm frame/sway parts phải kiểm nhưng không cộng trùng primary/atlas. Thư mục `_gemini`, `_gemini-rejected`, `jobs` và previous finals là lịch sử, không phải delivery hiện hành.

Các gói khác cũng nằm trong handoff:

- `batch-00` đến `batch-09-octopath`: baseline/style và art đã duyệt; không tự vẽ lại tất cả. Forest/city/beach/ship dùng các batch này và gói bổ sung, không kết luận thiếu vì không có batch-11 tương ứng. So hash/version trước khi kế thừa approval.
- `batch-10-octopath`: 15 primary + 13 auxiliary records; batch-10 và batch-11 không dùng làm style anchor thay cho batch 00–09 đã duyệt.
- `garden-a`: 30 asset. **Hiện Claude đã duyệt 25/30**, khác log Codex cũ. Đọc `garden-a/REVIEW-CLAUDE-20261109.md` và manifest: 5 bị trả là `gd-trunk-seg-01`, `gd-trunk-seg-02`, `gd-seal-strip`, `gd-seal-strip-lit`, `gd-pillar-vein-01`. Trunk sai exact vertical seam; seal sai lề và QA bbox; vein-01 chỉ 1 màu. Review có thêm hygiene cần sửa. Giữ quyết định Claude hiện hành, không reset tất cả thành pending.
- `p01-v1.1.0-b1/redo/{A,B,C,D}`: **39 candidate**, lần lượt 13/11/8/7; Điền Trang, Phòng thú cưng, Huyết Chiến Đài, Vương Cung. Có contact sheet xanh/đỏ, review viền, tile repeat/offset. So với predecessor `p01-v1.1.0-b1/{A,B,C,D}`, tránh cộng trùng và xác định replaces chính xác.
- Các gói bổ sung được inventory ghi nhận: `batch-12-city` 41, `batch-13-release` 14, `p01-release-art-20261023` 110; `octopath-s01-s27-20261029` dùng schema riêng với 45 generated và 24 pending. Hãy xác định liên hệ plan, đối chiếu brief của từng gói; tách phần UI/actor/NPC ngoài map art thành phụ lục phụ thuộc, không bỏ sót hoặc cộng vào % map coverage.

Session gần đây tập trung World Tree:

- Candidate đã thay: portal dormant/active, `world_tree-prop-07` nấm, `world_tree-prop-10` bậc cành, `world_tree_gate-landmark-01` hoa. Raw cũ và previous finals giữ trong asset/jobs. Cặp portal mask giống nhau; stairs là sáu tread rời, cần xem có đọc thành cầu thang không; mushroom còn coarse ở map-scale.
- Hoa attempt 04 đang là candidate final, 384²/40 màu/alpha nhị phân/lề 8px; attempt 05 không thay final vì quá glossy/vàng, viền nặng, lề 7px. Attempts 01–03 cũng không là delivery hiện hành.
- `world_tree-edge-03` vẫn **chưa có candidate đăng ký**. Attempts 01–16 bị self-reject vì seam/style/magenta/cadence; giữ trong `jobs/edge-03-attempt-*-study/`. Không xem chúng là hoàn thành. Kiểm bằng repeat thật sau correction ở trên.
- `qa-compositions.py/json` và ba `qa-composition-*.png` là mockup QA trên map gốc, scale/anchor xấp xỉ, **không phải scene dựng hoàn chỉnh**. Chúng chỉ overlay một số prop; không thay thế toàn bộ nền/asset gốc, không đặt golden-flower candidate. Preview hoa riêng nằm ở `jobs/landmark-flower-redraw-attempt-04-study/map-scale-world_tree_gate.png`. Không dùng hoa có sẵn trong ảnh nền làm bằng chứng candidate mới hợp style.

## 4. Nghiệm thu cụ thể

Chạy check phù hợp và đọc phạm vi checker. Kết quả cũ 626 asset / 0 lỗi / 0 cảnh báo chỉ là batch-11 gate tại checkpoint, **không chứng nhận Garden, P01 redo hay mọi gói phụ**; audit snapshot này đã phát hiện lệch hash. Ghi lệnh, phạm vi, thời điểm và lỗi thực tế. Không sửa gate/waiver để đạt.

Mở contact sheets để định hướng rồi xem từng asset ở game-scale và 4× caro/tối; mỗi asset chưa xem phải ghi `CHƯA_XEM`, không duyệt hàng loạt. Với sàn xem 3×3 thật + offset, edge/backdrop xem 3×1 thật, kiểm viền 8px/lưới/chu kỳ; với FX/state pair xem animation/registration/mask; với tree split xem lắp canopy/trunk và pivot. So với ảnh gốc và style assets đã duyệt cùng loại. Kiểm density/world scale, số màu 33–48 theo Master, alpha, fringe, pixel rời, outlines, ánh sáng và việc nướng glow/shadow.

Cho mỗi ID kết luận một trong: `DUYỆT`, `SỬA_ĐÓNG_GÓI_METADATA`, `VẼ_LẠI`, `THIẾU_CHƯA_CÓ`, `TÁI_DÙNG_HỢP_LỆ`, `CHƯA_XEM`. Ghi file/hash được xét, lỗi quan sát, bằng chứng preview, map bị ảnh hưởng và tiêu chí để đóng. Tách thiếu artwork, lỗi artwork, lỗi metadata và thiếu scene proof. Không đồng nhất đủ candidate với đủ art được duyệt hoặc map đã hoàn thiện.

## 5. Roadmap toàn bộ plan và đầu ra bắt buộc

Lập bảng coverage đủ 92 map: kit, map_id, ảnh nguồn, shared kit assets, landmark riêng, portal/marker/FX/backdrop, ID dùng lại, artwork còn thiếu, redraw cần làm và bằng chứng map-scale còn thiếu. Tái dùng phải có nguồn hợp lý; không tự tạo landmark độc nhất nếu ảnh nguồn không chứng minh. NPC là dependency riêng theo roster/checklist, không trộn với scope environment.

Tám kit đang chưa có batch-11 asset theo inventory/checklist là **tower → maze → guild → battlefield → maya → dungeon → arena2 → minigame** (23 map). Đối chiếu thêm gói phụ trước khi chốt thiếu thật. Rà đủ từng hàng chưa vẽ của từng kit, không chỉ ghi “vẽ kit X”. Chín kit batch-11 đã có và bốn kit baseline cũng phải có verdict/coverage.

Roadmap theo ưu tiên: sửa bằng chứng/provenance/metadata ảnh hưởng nghiệm thu; chốt redraw của kit đã có (World Tree/Garden và các lỗi floor/edge/backdrop đã review); hoàn tất các kit chưa có theo thứ tự plan. Được đề xuất batch nhỏ để tránh lặp hàng chục lần cùng lỗi, nhưng không bỏ yêu cầu chất lượng hoặc tự giảm phạm vi. Mỗi task phải có ID asset, map sử dụng, path output, NEW/REDRAW/FIX, kích thước/world scale/pivot, frame/mask/sway, reference gốc và style cụ thể, lỗi cần tránh, prompt vẽ copy-paste được, dependency, thứ tự và acceptance có thể đo + review hình. Tách hard requirement với đề xuất của reviewer.

Viết kết quả vào:

1. `.ai/design/map-checklists/REVIEW-CLAUDE-20261109-HANDOFF.md`: verdict, evidence, phạm vi đã xem/chưa xem và mâu thuẫn tài liệu.
2. `.ai/design/map-checklists/ASSET-VERDICTS-20261109.csv`: một dòng/ID/version, không bỏ asset; ghi replaces/reused_from để không cộng trùng.
3. `.ai/design/map-checklists/MAP-COVERAGE-20261109.csv`: đủ 92 map.
4. `.ai/design/map-checklists/ROADMAP-ART-92MAPS-20261109.md`: thứ tự milestone/batch và prompt thực thi chi tiết.
5. `.ai/design/map-checklists/ROADMAP-ART-TASKS-20261109.csv`: từng task/asset, ưu tiên, dependency, acceptance.

Sau audit cập nhật trạng thái checklist/README thủ công theo bằng chứng, giữ lịch sử và approvals hợp lệ. Không commit/push, sửa runtime/client, restart server hoặc sinh artwork trong đợt audit này. Nếu phát hiện phạm vi bổ sung ngoài 92 map, ghi phụ lục riêng.

Báo lại số asset duyệt/redraw/fix/missing/chưa xem theo mẫu số rõ, coverage 92 map, 3 asset yếu nhất mỗi kit và batch vẽ đầu tiên có thể giao ngay cho Codex. Chỉ nói 100% art plan khi mọi yêu cầu asset của 92 map đã có verdict hợp lệ và không còn task redraw/new/fix bắt buộc; scene/gameplay integration được báo riêng theo scope gốc.
