# Review kích thước và art late game — 2026-10-08

Status: owner đã chốt A cho hướng size ngày 2026-10-08; tỷ lệ cụ thể và polish từng loài còn đang debate.

## Phạm vi và bằng chứng

- Đo idle đầu tiên của 152 loài: alpha ≥128 để thống kê độ đọc, không sửa pixel hoặc xóa alpha. Hash atlas trong measurements.json.
- Xem idle của 104 loài 1–3★; xem contact sheet đủ 20 frame của 48 loài 4–5★, có 13 Special 5★ và 4 Special 4★.
- So sánh hình gốc APK qua portrait đối với nhóm 4–5★. Đo vùng frame đầu từ frames.tres gốc của đủ 152 loài. Các góp ý hình thể mơ hồ vẫn phải đối chiếu toàn atlas nguồn khi chuẩn bị prompt sửa.
- Đây là review hình tĩnh, không phải chứng nhận playback, motion interpolation, timing hoặc độ đọc trong battle thật. Các contact sheet thu nhỏ dùng để phát hiện vấn đề; trước sửa phải mở atlas native.
- Giữ bản gốc APK và lưu anchor cũ để so sánh; owner đã yêu cầu review và sửa cả hai anchor nếu cần. Chỉ thêm tài liệu/ảnh chẩn đoán; không đổi candidate selection, code, runtime hoặc server.

## Size hiện tại

| Star | Số loài | Chiều cao silhouette idle: min / median / max (px) |
|---|---:|---:|
| 1 | 50 | 75 / 133.5 / 172 |
| 2 | 30 | 78 / 129 / 167 |
| 3 | 24 | 104 / 132 / 175 |
| 4 | 21 | 87 / 139 / 174 |
| 5 | 27 | 110 / 150 / 242 |

Chiều cao gồm cánh, vũ khí, đuôi hoặc FX nếu có; không phải đo riêng cơ thể. Hai anchor được tính trong tier 5 và có canvas/tỷ lệ khác; không dùng chúng để khẳng định mọi atlas tuân thủ geometry mới.

Frame gốc lấy từ bản trích xuất có chiều cao silhouette min/median/max: 1★ 23/40/135; 2★ 28/42.5/136; 3★ 34/45/153; 4★ 36/50/65; 5★ 49/63/177. Kết quả gợi ý median tăng theo star, nhưng raw frame có độ phân giải/margin khác nhau. Không đủ chứng minh kích thước render game gốc hoặc rằng mọi pet 1–3★ bằng nhau.

## Scaling trong Godot

- room.gd:388–400: factor = min(height / sprite.get_height(), 94 / sprite.get_width()). Scale theo toàn texture, không theo thân hay vùng nhìn thấy.
- Battle dùng height 62 cho pet thường, 80 cho hai anchor; world pet đi theo 46/60, wild 48. Với ô 281px, pet thường cao 110px chỉ hiện khoảng 24px khi height=62; pet 170px hiện khoảng 38px. Đây là phép tính giả định khi route atlas vào renderer hiện tại, không phải ảnh đã kích hoạt 150 redraw.
- Các vị trí battle cách nhau 68px theo trục dọc. Cần review khoảng cách, tên/HP, selection ring và bounds trước khi tăng size; tăng height đơn thuần vẫn bị cap width 94.
- room.gd:46 đã dùng TEXTURE_FILTER_NEAREST. Godot docs: https://docs.godotengine.org/en/stable/classes/class_canvasitem.html#enum-canvasitem-texturefilter . Nearest giữ kiểu pixel, không tạo chi tiết mới; scale lẻ có thể làm độ dày pixel không đều.
- Không crop/normalize theo bbox mỗi frame: sẽ gây nhảy size/pivot. Dùng một scale thống nhất mỗi loài mỗi context, pivot cố định + offset pose nếu cần, và kiểm tra envelope của cả 20 frame.

## Hướng size A đã được owner chọn — tỷ lệ thử chưa phải runtime config

Đề xuất A: lấy cảm giác khối thân 1–3★ làm 1.0, cho sai lệch khoảng ±15% theo dáng; 4★ khoảng 1.15–1.30; 5★ thường 1.30–1.50; Special 5★ khoảng 1.45–1.65 với ngoại lệ chủ đích. Đây là tỷ lệ thử art direction, không phải số pixel cuối cùng.

Pet ngang đo theo khối vai/thân và chiều rộng; pet bay theo thân với hover pivot; vũ khí/cánh/đuôi là envelope phụ. Không kéo giãn x/y riêng, không làm mọi con cùng chiều cao. Ngựa Bùn Cỏ và tiên hoa có thể nổi bật nhờ diễn xuất/màu/silhouette thay vì to nhất.

Cấu hình tương lai có thể gồm species_id, world_scale, battle_scale, preview_scale, pivot, hover_offset và envelope. Đây chỉ là tên gợi ý, chưa là schema chuẩn. Art scale không tự đổi damage, collision, capture hoặc server RNG.

Contract cũ ghi “Five-star … never larger sprites”. Yêu cầu mới của owner cho phép cảm giác pet late game lớn hơn; cần ghi quyết định mới sau debate. Atlas có thể vẫn cùng 281px/cell, khác kích thước hiển thị và mức đầu tư chi tiết. Không tăng canvas hoặc override containment ngầm.

## Góp ý từng loài 4–5★

Các nhãn dưới đây là ưu tiên polish mỹ thuật, không phải lỗi gameplay hay verdict loại bỏ bản đang được owner thích.

| ID | Loài | Tier | Hướng xử lý | Quan sát và đề xuất |
|---|---|---|---|---|
| species_0015 | Tử Thần | 4★ normal | Polish + size | Dáng lưỡi hái và áo choàng rõ; thân quá nhỏ. Tăng cảm giác hiện diện, tách mắt/mặt khỏi tóc và sừng; giữ lưỡi hái một chiếc. |
| species_0016 | Pharaon | 4★ normal | Giữ + polish nhẹ | Mặt, gậy và trang phục rõ. Giảm điểm sáng vụn trên thân, làm rõ chất liệu vải so với giáp; ưu tiên nhịp gậy và đầu khi idle. |
| species_0017 | Rồng Xương Băng | 5★ normal | Polish | Silhouette xương tốt; xương trắng và màng cánh nâu chưa gợi băng. Đối chiếu palette APK trước khi thử bóng lạnh; không tự biến thành rồng xanh hoặc thêm băng giáp. |
| species_0018 | Nữ Vương Bạch Cốt | 5★ normal | Giữ + polish nhẹ | Vương miện, rìu và váy có nhận diện. Làm rõ hốc mắt, bàn tay và khối váy khi thu nhỏ; giữ đúng một rìu và hai tay. |
| species_0019 | Nữ Đế Minh Giới | 5★ special | Ưu tiên cao | Màu xanh ngọc, áo tím, trượng đỏ tạo nhận diện riêng. Tách mắt/miệng khỏi trang sức, gom các mảng tóc; cast cần dáng thân và tay rõ hơn, không chỉ tăng lửa. |
| species_0020 | Thủ Lĩnh Hắc Ám | 5★ special | Ưu tiên cao | Kỵ sĩ và thú cưỡi đang dễ hòa thành một khối xanh. Tách đầu thú cưỡi, đầu kỵ sĩ và kiếm bằng sáng tối; áo choàng có trọng lượng, bước thú cưỡi có nhịp rõ. |
| species_0035 | Trưởng Lão Người Cây | 4★ normal | Polish + size | Khuôn mặt gỗ có cá tính nhưng dáng nhỏ. Tách râu, mắt, miệng khỏi lá; tăng cảm giác trưởng lão qua dáng và nhịp chuyển động, giữ cấu trúc APK. |
| species_0036 | Hoa ăn Thịt Người Ba Đầu | 4★ normal | Giữ + polish nhẹ | Ba đầu và răng đọc được. Cho ba cổ có nhịp lệch nhau khi idle/cast; làm rõ đầu trước và sau, tránh cả ba dính thành một mảng. |
| species_0037 | Độc Đằng Nữ | 5★ normal | Review lại anchor | Độc Đằng Nữ là base style, không phải atlas hoàn thiện được miễn review. Kích thước 1122×1402 không đạt contract; kiểm tra padding, pivot và diễn xuất trước khi chọn bản sửa. |
| species_0038 | Tinh Linh Bách Hoa | 5★ normal | Giữ + polish nhẹ | Mặt và tóc hoa đáng nhớ. Cánh xanh dễ bị chìm khi nhỏ; gom gân cánh, làm rõ tay cầm gậy, giữ vẻ nhẹ nhàng. |
| species_0050 | Hải Long Ba Đầu | 4★ normal | Polish | Hai đầu xanh/tím còn dày chi tiết quanh cổ. Tách hai mặt và cổ bằng sắc độ; giữ HAI đầu theo hình APK, không thêm đầu thứ ba theo tên. |
| species_0051 | Long Vương Hắc Ám | 4★ normal | Giữ + polish nhẹ | Khối rồng và cánh đỏ rõ. Giảm texture chấm trên vảy, nhấn mắt và hàm; làm nhịp thở nặng hơn khi idle. |
| species_0052 | Thánh Rồng Thái Cổ | 5★ normal | Ưu tiên cao | Thân chỉ cao 110px trong ô 281px, dáng rất compact so với tier 5. Scale giúp hiện diện; cần polish mặt, ngực, cánh và tư thế để có khí chất thái cổ, không tự thêm sừng/giáp. |
| species_0066 | Đại Ác Ma | 4★ normal | Giữ + polish nhẹ | Sừng, cánh và giáp rõ. Tách tay khỏi phần thân đỏ, giữ mảng giáp lớn; tránh highlight vàng phủ toàn bộ khiến khó đọc mắt. |
| species_0067 | Ma Vương Địa Ngục | 4★ normal | Polish | Giáp vàng và da đỏ đang cạnh tranh. Chọn mặt, sừng và ngực làm điểm nhấn; giảm sáng trên các phần phụ, giữ dáng rộng nặng. |
| species_0068 | Thanh Long | 4★ special | Polish + size | Special 4★, không phải 5★. Dáng rồng dài nên ưu tiên chiều rộng và thân, không kéo cao. Tách râu, sừng và bờm khỏi nền xanh. |
| species_0069 | Trụy Thiên Sứ | 5★ normal | Ưu tiên cao | Thân 115px; cánh và kiếm rõ hơn mặt, chưa nổi bật ở tier 5. Làm rõ đầu, ngực, tay cầm kiếm và phân lớp lông cánh; giữ một kiếm đỏ và camera trái. |
| species_0084 | Tinh Tinh Rock | 4★ normal | Giữ + polish nhẹ | Tóc và biểu cảm đã có hồn. Giữ nét hài hước, thêm trọng lượng cho nắm đấm/động tác; không biến thành gorilla hiện thực. |
| species_0085 | Đại Tuyết Quái | 4★ normal | Giữ + polish nhẹ | Lông trắng và dáng hiền khác Người Tuyết Viễn Cổ. Tách mặt khỏi lông bằng bóng cụm; giữ hoa nhỏ và dáng APK, không ép thành dữ tợn. |
| species_0086 | Gấu Trúc Ma Pháp | 4★ normal | Giữ + polish nhẹ | Mặt trắng, thân tím và gậy xanh dễ nhận. Làm mắt/miệng rõ hơn; cast bằng tay/thân trước khi cân nhắc FX. |
| species_0087 | Bạch Hổ | 4★ special | Polish + size | Special 4★. Thân ngang chỉ cao 87px, không nên nâng đến bằng chiều cao chim. Scale theo khối vai/thân, làm mắt và sọc rõ; giữ giáp vàng. |
| species_0088 | Sói Xích Viêm | 5★ normal | Giữ + polish nhẹ | Mặt và bờm lửa mạnh, đọc được. Phân biệt lửa với lông và da; tránh sáng đều toàn bộ bờm, giữ phản ứng thân khi tấn công. |
| species_0103 | Chim Đại Phì | 4★ normal | Giữ + polish nhẹ | Dáng tròn hợp tên và APK; có mắt/cá tính. Giữ khối tròn, chia lớp lông lớn, không ép chim này thành chim săn mồi cao gầy. |
| species_0104 | Chim Đa Đa | 4★ normal | Giữ + polish nhẹ | Mỏ, mào và cánh đỏ tím rõ. Gom đầu lông nhỏ thành cụm; tách mắt khỏi mào và chuyển động cánh khỏi đuôi. |
| species_0105 | Chu Tước | 4★ special | Giữ + polish nhẹ | Special 4★. Đuôi cuộn là nhận diện chính; giữ thiết kế riêng với Đảo Thiên Đường. Làm mắt/mỏ rõ, không thêm bộ đuôi xanh của anchor. |
| species_0106 | Chim Cú Địa Ngục | 5★ normal | Polish | Dáng hybrid chim/rồng dễ nhận. Đầu xanh, cổ xanh và cánh tím cạnh tranh; giảm bóng mượt cánh, nhấn mắt/mỏ và lớp lông cổ bằng pixel clusters. |
| species_0107 | Đại Bàng Vàng | 5★ normal | Giữ + polish nhẹ | Cánh sáng và đầu vàng cam rõ. Giữ đúng hình APK, không sửa thành đại bàng hiện thực; làm móng, mỏ và gốc cánh chắc hơn. |
| species_0122 | Trùng Hốt Lỗ | 4★ normal | Polish | Hình hồng độc đáo nhưng độ hoàn thiện vật liệu thấp hơn nhiều loài cùng tier. Tách bụng, xúc tu, mặt và bóng cụm; xác minh mắt trắng từ nguồn trước khi đổi biểu cảm. |
| species_0123 | Trùng Gai Nhọn | 4★ normal | Giữ + polish nhẹ | Mắt, miệng, gai có cá tính. Tách chân với gai phía dưới, giảm chấm sáng vụn; giữ khối gai hữu cơ. |
| species_0124 | Trùng Bất Tử Địa Huyệt | 5★ normal | Polish | Hàm và chân chồng nhau khi nhỏ; cánh trong nổi hơn đầu. Tách hàm khỏi chân bằng viền/sắc độ, giữ thân giáp cứng và cánh nhẹ. |
| species_0125 | Nhện Phu Nhân | 5★ normal | Polish | Mặt nhỏ, cánh lớn nhiều gân. Tăng độ đọc của mắt/tay và nhóm gân cánh thành mảng; giữ đặc điểm APK dù tên dễ gây hiểu nhầm thành nhện thuần túy. |
| species_0126 | Trùng Mẫu Mào Vàng | 5★ special | Ưu tiên cao | Vương miện tốt, nhưng mặt nhỏ giữa mào và bụng đỏ sáng. Mặt là điểm nhấn thứ nhất, bụng/chân thứ hai; giảm bóng mượt bụng, nhấn khớp chân và dáng nữ vương. |
| species_0137 | Ma Gương Thủy Tinh | 4★ normal | Giữ + polish nhẹ | Gương đỏ và bộ xương có silhouette khác biệt. Tách xương bàn tay/chân và mặt gương; không tự thêm mặt người vào gương. |
| species_0138 | Thú Lớn Dung Nham | 4★ normal | Giữ + polish nhẹ | Nắm đấm đá và khe dung nham rõ. Giảm sáng rải đều; nhấn mắt và vài khe chính, cho thân nặng và nhịp lún khi ra đòn. |
| species_0139 | Huyền Vũ | 4★ special | Giữ + polish nhẹ | Special 4★. Mai vàng và thân đỏ tím rõ, nhận diện riêng. Phân lớp mai/cổ/chân, ưu tiên chiều rộng; giữ thiết kế APK thay vì tự đổi thành rùa đen. |
| species_0140 | Nhân Sư | 5★ normal | Giữ + polish nhẹ | Giáp vàng tím, mắt xanh và tư thế ngồi đọc được. Tách mặt khỏi mũ, phân biệt kim loại với thân; giữ vẻ trang nghiêm bằng nhịp động tác. |
| species_0141 | Totem Thượng Cổ | 5★ normal | Polish | Các hoa văn và mắt dày, dễ thành khối nâu. Chọn một mặt chính để dẫn mắt, gom hoa văn phụ; giữ hình totem và cấu trúc nguồn. |
| species_0142 | Thần Tướng Cự Ma | 5★ special | Ưu tiên cao | Giáp, khiên và thân đỏ nổi; đầu lại thiếu độ đọc. Làm rõ đầu/mặt theo nguồn, tách ngực khỏi vai, giữ tỷ lệ khối nặng; không tự thêm đầu hoặc mặt khi APK chưa rõ. |
| species_0143 | Thần Đèn | 5★ special | Polish vừa | Biểu cảm và đèn rõ, phù hợp chất tinh nghịch. Da xanh đang bóng tròn/mượt hơn anchor; gom highlight thành cụm pixel, tăng diễn xuất mắt và bàn tay. Giữ một đèn. |
| species_0144 | Linh Tiên Hoa Hương | 5★ special | Polish vừa | Màu và silhouette cánh hoa mạnh. Cánh hoa quá sáng có thể át mắt/mặt; hạ nhấn phần sau, làm rõ tay và tầng váy xanh. Giữ vẻ dịu, không ép thành chiến binh. |
| species_0145 | Cây Cự Linh | 5★ special | Polish vừa | Cây với hai khối trụ gỗ có nhận diện mạnh. Lá, gỗ và đá nhiều texture; gom cụm, làm rõ mắt/miệng và vai. Giữ HAI trụ đúng nguồn, không tự đổi thành đại bác. |
| species_0146 | Ma Vương Hút Máu | 5★ special | Ưu tiên rất cao | Thân, cánh và đao đang mềm/bóng hơn hai anchor. Vẽ polish cụm pixel, phân lớp hàm-ngực-tay-cánh, tách kim loại khỏi da; giữ một đao và dáng APK. Đây là ứng viên đầu tiên nên debate sâu. |
| species_0147 | Người Tuyết Viễn Cổ | 5★ normal | Polish | Lông và ngà rõ nhưng bóng nhỏ nhiều. Gom cụm lông, nhấn mắt/ngà/khối vai; giữ một gậy đúng tay và dáng nặng khác Đại Tuyết Quái. |
| species_0148 | Ngựa Bùn Cỏ | 5★ special | Polish vừa | Dễ thương, biểu cảm riêng và yên xanh rõ. Không cần ép dữ hoặc khổng lồ để chứng minh Special. Nâng mắt, cấu trúc lông và chân; giữ tính cách vui, nhịp nhún/ngoái đầu đúng camera. |
| species_0149 | Thú Vàng Một Sừng | 5★ special | Ưu tiên cao | Sừng và bờm nổi nhưng thân vàng trắng hơi hòa, gần cảm giác pet thường. Tách mặt/ngực/chân, xây các cụm lông vàng rõ và dáng kiêu hãnh; không thêm cánh/giáp để làm hiếm. |
| species_0150 | Đảo Thiên Đường | 5★ special | Review lại anchor | Đảo Thiên Đường là base style. Kích thước 1122×1402 không đạt contract; hàng hurt/down vẫn bay/đứng, cần pose gục rõ. Giữ nhận diện nguồn, review lại đủ 20 frame và padding. |
| species_0151 | Đại Vương Bọ Cạp | 5★ special | Ưu tiên cao | Càng và đuôi mạnh nhưng mặt/thân tím dày chi tiết. Tách mặt/giáp bụng/khớp chân, giữ một đuôi và ngòi; nâng dáng săn mồi qua anticipation, không chỉ tăng kích cỡ càng. |
| species_0152 | Chim Ái Thần | 5★ special | Ưu tiên cao | Cánh tím đẹp nhưng mặt, tóc vàng và tay nhỏ dễ chìm. Làm mắt/miệng và bàn tay đọc được, phân lớp cánh/tóc/thân; tăng diễn xuất dịu dàng, không tăng độ gợi cảm hoặc đổi trang phục. |

## Thứ tự debate và chuẩn nghiệm thu polish

1. Chốt size theo cảm giác thân và bố cục battle; thử pet đứng, pet ngang, pet bay với hai anchor.
2. Debate Special 5★ trước: 0146 → 0142 → 0020 → 0126 → 0019 → 0151 → 0149 → 0152 → 0145 → 0143 → 0144 → 0148; 0150 phải review và sửa như các pet khác.
3. Debate 5★ thường ưu tiên: 0052, 0069, 0017, 0124, 0125, 0141, 0147; sau đó nhóm giữ + polish nhẹ.
4. 4★ ưu tiên size/độ đọc: 0015, 0035, 0050, 0068, 0087, 0122; tiếp đến các góp ý còn lại.

Mỗi pet chốt: (a) nhận diện nguồn cần giữ; (b) tính cách thể hiện; (c) điểm nhấn nhìn ở size gameplay; (d) cụm pixel/vật liệu cần polish; (e) nét riêng attack/cast; (f) tỷ lệ và pivot; rồi mới tạo prompt. Reference identity chỉ APK của chính pet; hai anchor chỉ style. Không lấy redesign của pet khác làm identity.

Kiểm tra sau sửa: mặt/điểm nhấn đọc được tại size gameplay đã chốt, nền sáng/tối; 20 pose giữ hình thể/phụ kiện/camera; attack và cast có diễn xuất khác nhau; loop 4→1 mượt; down không thay anatomy; mechanical containment/lineage/hash; review playback thật, sau đó owner duyệt trước runtime activation.

## Boards

- 4star.png, 5normal.png, 5special.png: original portrait + selected idle.
- late-01.png … late-12.png: đủ 20 frame của 48 loài 4–5★.
- early-01.png … early-03.png: idle 104 loài 1–3★.
- measurements.json: 152 atlas paths/hash, class/star/idle bounds; original-measurements.json: 152 source first-frame bounds.

## Quyết định owner 2026-10-08

Chọn A: tăng size theo tier, có ngoại lệ theo loài. 1–3★ cùng cảm giác kích thước, 4★ lớn hơn nhẹ, 5★ lớn rõ hơn; Special 5★ nổi bật theo dáng loài, giữ tính cách dễ thương nếu phù hợp. Các tỷ lệ phải thử trên màn battle trước khi chốt. Quyết định này cho phép khác biệt kích thước hiển thị, thay thế hạn chế cũ không tăng kích thước cho 5★; không phê duyệt mọi đề xuất polish, pixel size cụ thể hoặc runtime activation.

## Owner correction — 2026-10-08

Owner chọn A cho Ma Vương Hút Máu: nặng, hung dữ, nhát đao có trọng lượng. Owner xác nhận hai anchor chỉ là base để generate, chưa chuẩn hoàn thiện; trong scope review này phải đánh giá và sửa nếu cần. Các đề xuất giữ/khóa tuyệt đối anchor ở review trước được thay thế. Lưu các bản cũ làm bằng chứng lịch sử, tạo bản sửa riêng và không thay runtime trước review.
