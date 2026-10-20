# P13 — Closure (design)

**Trạng thái: ĐÓNG thiết kế 2026-10-20.** Owner gửi kết luận *duyệt toàn bộ* cho candidate V7.1. Đây là đóng phase thiết kế; **runtime, migration và cân bằng chiến đấu chưa kích hoạt/chứng nhận.**

## Candidate được duyệt

- Gói: [roster-review-package.json](roster-review-package.json), SHA-256 `57c077969bd78a432e2e86c54f799b5fcf2ff070a420335cfaf52a5dd7b2e468`, revision `P13-candidate-v7.1-20261019`.
- Phản hồi owner: `review/responses/57c07796…2e468.json` — 18/18 nhóm D01–D18 *approved*, verdict *approved* (version 3, nguồn `owner_chat_final_verdict`).
- Quyết định mang từ hash cũ có ghi `carried_from`; D04 (sau buff signature) và D15 do owner duyệt trong chat 2026-10-19; kết luận cuối 2026-10-20.
- Nội dung: 160 loài (152 đóng băng + 6 Normal 5★ + 2 Special Hybrid 5★, ID `species_0153…0160`), 97 skill (9 signature độc quyền), 28 recipe candidate, 32 acceptance scenarios, Element chart (Hỏa>Phong>Địa>Thủy>Hỏa ×1.25/×0.8; Quang↔Âm ×1.25), 6 slot, SR `p_final = p_base×(1−0.8×SR/(SR+100))`.
- Hai signature mới: `dual_seal_light` → `species_0159`, `inverse_seal_dark` → `species_0160` (1.50 lực đánh, MP28, CD3, Lv40, rank1, không kế thừa).

## Nguyên tắc owner chốt cho chi phí học (2026-10-20)

Skill càng mạnh học/nâng càng tốn nhiều **vàng**; vàng là tiền tệ farm. Behavior contract đã có công thức theo hướng này: rank1 = `20 + 10×learn_level` vàng, rank2 = 3×rank1, rank3 = 6×rank1 (mỗi lần nâng). Skill mạnh nhất (Lv40, gồm 9 signature và các "super") = 420 vàng ở rank1. Đối chiếu 97 skill: chi phí tăng đơn điệu theo `learn_level`; skill đơn thể mạnh thường ở level cao hơn AoE yếu từng mục tiêu. Phần còn mở là **quy mô** vàng so với thu nhập farm (P15) và nguồn/sink vàng (P19), không phải công thức.

## Việc P13 không sở hữu (chuyển phase sau)

| Hạng mục | Chủ |
|---|---|
| Cân bằng chiến đấu thực đo (hai signature 1.50, SR/cleanse, ±50% clamp) — số liệu đang là thiết kế, chờ playtest | P02, P07 |
| Pacing vàng: thu nhập farm vs chi phí học 420/1260/2520, relearning | P15, P19 |
| Art 8 loài mới, migration 14 → 160 (P10-O08) | P10 / P16 |
| Effect budget, trang bị | P14 |
| Lifecycle/snapshot, recipe cost/xác suất/Plus | P16, P20 |
| Runtime: nạp 97 skill + 160 pool, thay catalog 14 loài / 29 skill / 6 recipe | gate migration riêng |

## Kiểm chứng

- `tools/content/test_p13_design.py` 15, `test_p13_roster_review.py` 14, `tools/p13_review/test_server.py` 8 — pass; `test_p10_extension` 10 vẫn pass (catalog 160 giữ key proposal + `stable_id`).
- Tái tạo: `python3 tools/content/p13_roster_review.py` (ghi package, catalog 160, skill catalog 97, feedback doc). Test P13 nằm trong `tools/check.sh`.
- Không có runtime code, không combat/economy certification, không 50 CCU.

## Tài liệu liên quan

[README](README.md) · [final spec](P13-final-spec.md) · [behavior contract](P13-behavior-contract.md) · [source audit](P13-source-audit.md) · [verification V7](P13-verification-v7.md) · [mapping P10](P13-to-P10-eight-species-mapping.json). Lịch sử bản cũ (95 skill, 152 loài, review package cũ) giữ trong `evidence/` và các file trước V7.
