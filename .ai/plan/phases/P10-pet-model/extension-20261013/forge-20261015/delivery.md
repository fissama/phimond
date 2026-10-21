# Sprite Forge — mẫu nhân vật để duyệt, 15/10/2026

## Quy trình hiện hành — chủ dự án đính chính 15/10/2026

**Không dùng image-to-video.** Phimond dùng một PNG tĩnh chứa 20 pose khác nhau, 4 cột ×5 hàng. Game lấy từng ô để phát animation; mỗi animation có4frame. Năm mẫu một pose chỉ là reference thiết kế. Thiếu API/CLI video **không phải điểm nghẽn**. Các đoạn mô tả cần nguồn video bên dưới là lịch sử của hướng hiểu sai, đã được mục này thay thế.

Đã đối chiếu atlas Thần Đèn0143, Đại Vương Bọ Cạp0151 trong bộ152 đã khóa và atlas0154/0156/0158 đã duyệt, contractP10, preview_p10_redraw.py và reference_art.gd. Theo thứ tự hàng: idle,move,basic,skill,hurt→fullydown. Hai hàng đầu lặp; ba hàng sau một lần và giữ framecuối. OutputRGBA1124×1405,cell281,alpha[22,259),hướngtrái. Không đổi contract sangvideohoặc chỉmộtpose.

Sprite Forge được dùng cho lập spec/pose, kiểm tràn ô, identity, scale và đóng gói; yêu cầu video trong skill được ghi đè cho dự án này bởi chỉ dẫn trực tiếp của chủ dự án. Giữ nguyên skill toàn cục. atlas-jobs.json chuẩn bị5loài theo pipelinePNG, chưa tuyên bố đã vẽ xong20frame. Không chọn/kích hoạt runtime.

## Cập nhật sau khi chủ dự án duyệt mẫu

Chủ dự án đã duyệt 4 mẫu nguồn Hươu, Tinh Vân, Ma Nhãn và Ma Chủ trong chat; hash khóa tại owner-master-approvals.json. Chỉ Long Thần cần sửa cánh. Bản mới species_0159/master-wing-v2.png dùng cánh giáp ngà mảnh viền vàng, điểm ngọc, vuốt ra sau; giữ hai tay/chân nhỏ/hai đuôi và hai ấn. Bản cánh này chưa được chủ dự án duyệt. Bản trước vẫn giữ nguyên master-proposal.png.

Đã chạy Forge master_still.py approve trên 4 nguồn được chủ dự án duyệt, xuất approved-master-v1/master.json và master_rgba.png. Đây là chuẩn hóa kỹ thuật cho nguồn video sau này, không phải atlas hay animation đã xong. Nguồn đã duyệt giữ nguyên byte. Tinh Vân có cảnh báo framing nguyên văn: "the subject is too wide for the hero framing: scaled to fit the width, 760 px tall instead of 788 px". Giữ toàn bộ hình thay vì cắt đuôi/cánh; không tuyên bố tất cả warning đã hết.

Kiểm chứng bổ sung: wing-update-verification.json; review cánh đúng hash tại wing-v2-review.json/md. Route video vẫn chưa có, chưa chạy clip hoặc kích hoạt runtime.

Đã áp dụng generate2dsprite / generate2dmedia của Agent Sprite Forge: capability doctor, master spec, prompt builder và QC spill trên atlas cũ. Dùng công cụ ImageGen tích hợp (art_source=host_image) để tạo năm mẫu nhân vật một pose. Đây chưa phải atlas/animation hoàn thiện; không có master.json đã duyệt giả, không tự duyệt thay chủ dự án.

Xem [gallery mẫu](http://127.0.0.1:8126/). Ba atlas Thiết Giáp Long, Đao Ma Huyết Giáp và Hộ Vệ Thạch Linh giữ nguyên hash đã duyệt; 152 atlas gốc không chỉnh sửa.

## Đã tạo

- Hươu: gạc gỗ phân nhánh cong tự nhiên, bỏ trăng gắn lên đầu.
- Tinh Vân: giữ mẫu rồng xanh đêm trưởng thành. Nhiệm vụ hiệu ứng 5★ được ghi riêng trong motion-briefs.json; chưa giả là hiệu ứng combat đã hoàn thành.
- Ma Nhãn: bỏ rune nổi, khung mắt có miệng nanh tại con ngươi, sáu đầu xúc tu đọc rõ hơn trong mẫu tĩnh.
- Long Thần: hai tay, hai chân sau nhỏ, hai cánh gọn, hai đuôi và hai ấn ở đầu đuôi; thân không mang huy hiệu ấn cũ.
- Ma Chủ: tóc trắng ánh tím rẽ ngôi gọn và ánh mắt lạnh, giữ tuổi trưởng thành khoảng 20, cơ bắp, thương, giáp chân và màu tím.

Mỗi loài có source PNG RGBA, spec.json, prompt gốc do Forge tạo, host-prompt.txt đã điều chỉnh sang native alpha, proposal.json với SHA và reference hashes. Kích thước thật được ghi trong metadata (không khẳng định 1024 chỉ từ prompt). Model thực tế không được công cụ công bố; estimateUsd=null, giá không xác định. Source chưa qua pixel finish/quantization hay animation.

## Chưa hoàn tất và điểm nghẽn

1. Chủ dự án duyệt mẫu đúng hash trước. generate2dsprite/SKILL.md yêu cầu: “One approved master still per character, then one image-to-video clip per action”.
2. Doctor xác nhận không có route tạo video: không có XAI_API_KEY, ARK_API_KEY, FAL_KEY hoặc Grok CLI; host chỉ có image_gen/image_edit. Vì vậy chưa chạy video2dsprite/sprite_set, chưa xuất animation hay tuyên bố độ mượt.
3. Đã chuẩn bị motion-briefs.json: idle/move lặp; basic/skill/hurt→fully down một lần, giữ frame cuối. Sau khi có mẫu duyệt và route video, dựng từng hành động từ cùng master, kiểm root/scale/loop, tách FX rồi ghép trong vùng an toàn. Output cuối vẫn theo contract P10: RGBA1124×1405, 4×5 cell281, 20 frame khác nhau, alpha[22,259), hướng trái. Không thay bằng video runtime tự động.
4. Nguồn tĩnh có thể còn pixel alpha rất mờ ngoài silhouette và style cần kiểm sau finish; không xóa alpha để che lỗi atlas và không tự coi mẫu tĩnh đạt geometry 20 frame.

## QA và giới hạn

verification.json: kiểm SHA/mode/alpha của 5 nguồn, giữ đúng byte 3 atlas đã duyệt, gallery HTTP200, review roster160 HTTP200. Browser đã kiểm tải đủ 5 ảnh, chế độ96/192 và nền sáng/tối.

Doctor không phải PASS toàn bộ: scipy chưa có (dùng fallback numpy); resvg/codeart không có và không dùng; không có các API key và Grok CLI. Toàn bộ kết quả nguyên văn trong doctor.json.

QC bên dưới áp dụng **raw atlas cũ với regular grid mặc định**, không phải năm mẫu một pose và không phải chứng nhận atlas packed. safe_frame mặc định 15% khắt khe hơn inset22px của P10. Không chạy alpha-hygiene, không lọc largest-component và không sửa source để làm số PASS. Các cảnh báo/lỗi được giữ nguyên id/value/threshold/file trong qa-warnings-verbatim.json; strict numeric checks không thay được review anatomy/motion.

## Dịch vụ xem

- Mẫu Forge: PID45140, 127.0.0.1:8126, log /tmp/p10-forge-review.log.
- Review atlas trước: PID45139, 127.0.0.1:8125, log /tmp/p10-extension-review.log.
- Không thay game-server, DB hay chọn art runtime. Đây là bàn giao mẫu chờ duyệt, không phải đóng phase/sprint.

## Nguồn skill

Repo: https://github.com/0x0funky/agent-sprite-forge

Skill đã có sẵn trong ~/.codex/skills; bước cài mới dừng vì destination tồn tại, không ghi đè bản hiện có. Nội dung skill và các file shared đã được đọc/kiểm bởi doctor. Route native image được dùng vì không có API key; không giả là API hoặc video đã chạy.

## QA WARN/FAIL nguyên văn

File: .ai/plan/phases/P10-pet-model/extension-20261013/forge-20261015/qa-existing-ma-chu/sheet-qc.json

```json
[
  {
    "id": "cross_cell_components",
    "status": "fail",
    "value": 17,
    "threshold": 0,
    "cells": [
      [
        0,
        1
      ],
      [
        0,
        0
      ],
      [
        0,
        2
      ],
      [
        0,
        3
      ],
      [
        1,
        0
      ],
      [
        1,
        1
      ],
      [
        1,
        2
      ],
      [
        1,
        3
      ],
      [
        2,
        1
      ],
      [
        2,
        0
      ],
      [
        2,
        3
      ],
      [
        2,
        2
      ],
      [
        3,
        1
      ],
      [
        3,
        0
      ],
      [
        3,
        3
      ],
      [
        3,
        2
      ],
      [
        4,
        2
      ]
    ],
    "note": "solid parts crossing a cell line are cut or misassigned when the sheet is sliced"
  },
  {
    "id": "cross_cell_visible",
    "status": "fail",
    "value": 17,
    "threshold": 0,
    "note": "the same test on the visible edge (alpha > 16)"
  },
  {
    "id": "boundary_band",
    "status": "warn",
    "value": 4966,
    "threshold": 0,
    "note": "solid pixels within 6 px of a cell line; a different crop or rounding can cut them"
  },
  {
    "id": "safe_frame",
    "status": "warn",
    "value": 20,
    "threshold": 0,
    "cells": [
      [
        0,
        0
      ],
      [
        0,
        1
      ],
      [
        0,
        2
      ],
      [
        0,
        3
      ],
      [
        1,
        0
      ],
      [
        1,
        1
      ],
      [
        1,
        2
      ],
      [
        1,
        3
      ],
      [
        2,
        0
      ],
      [
        2,
        1
      ],
      [
        2,
        2
      ],
      [
        2,
        3
      ],
      [
        3,
        0
      ],
      [
        3,
        1
      ],
      [
        3,
        2
      ],
      [
        3,
        3
      ],
      [
        4,
        0
      ],
      [
        4,
        1
      ],
      [
        4,
        2
      ],
      [
        4,
        3
      ]
    ],
    "note": "owned art closer than 15% of the cell to its edge; ask for more margin next time"
  },
  {
    "id": "faint_specks",
    "status": "warn",
    "value": {
      "floor_px": 224097,
      "detached_components": 43
    },
    "threshold": 0,
    "note": "alpha haze and detached specks; process removes them with --alpha-hygiene both"
  }
]
```

File: .ai/plan/phases/P10-pet-model/extension-20261013/forge-20261015/qa-existing-ma-nhan/sheet-qc.json

```json
[
  {
    "id": "cross_cell_components",
    "status": "fail",
    "value": 16,
    "threshold": 0,
    "cells": [
      [
        0,
        1
      ],
      [
        0,
        0
      ],
      [
        0,
        2
      ],
      [
        0,
        3
      ],
      [
        1,
        1
      ],
      [
        1,
        0
      ],
      [
        1,
        2
      ],
      [
        1,
        3
      ],
      [
        2,
        0
      ],
      [
        2,
        1
      ],
      [
        2,
        2
      ],
      [
        2,
        3
      ],
      [
        2,
        2
      ],
      [
        3,
        1
      ],
      [
        3,
        2
      ],
      [
        4,
        2
      ]
    ],
    "note": "solid parts crossing a cell line are cut or misassigned when the sheet is sliced"
  },
  {
    "id": "cross_cell_visible",
    "status": "fail",
    "value": 15,
    "threshold": 0,
    "note": "the same test on the visible edge (alpha > 16)"
  },
  {
    "id": "boundary_band",
    "status": "warn",
    "value": 4518,
    "threshold": 0,
    "note": "solid pixels within 6 px of a cell line; a different crop or rounding can cut them"
  },
  {
    "id": "safe_frame",
    "status": "warn",
    "value": 20,
    "threshold": 0,
    "cells": [
      [
        0,
        0
      ],
      [
        0,
        1
      ],
      [
        0,
        2
      ],
      [
        0,
        3
      ],
      [
        1,
        0
      ],
      [
        1,
        1
      ],
      [
        1,
        2
      ],
      [
        1,
        3
      ],
      [
        2,
        0
      ],
      [
        2,
        1
      ],
      [
        2,
        2
      ],
      [
        2,
        3
      ],
      [
        3,
        0
      ],
      [
        3,
        1
      ],
      [
        3,
        2
      ],
      [
        3,
        3
      ],
      [
        4,
        0
      ],
      [
        4,
        1
      ],
      [
        4,
        2
      ],
      [
        4,
        3
      ]
    ],
    "note": "owned art closer than 15% of the cell to its edge; ask for more margin next time"
  },
  {
    "id": "faint_specks",
    "status": "warn",
    "value": {
      "floor_px": 103577,
      "detached_components": 47
    },
    "threshold": 0,
    "note": "alpha haze and detached specks; process removes them with --alpha-hygiene both"
  }
]
```

