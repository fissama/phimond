# Nhạc nền v1.0.x: nguồn miễn phí và prompt MiniMax (2026-10-29)

Client đã có bộ phát nhạc nền (`apps/client/src/ui/music.ts`): lặp theo map và theo trận, chuyển bài mờ dần, đoạn thắng (victory) phát một lần, âm lượng riêng ở Cài đặt → Âm thanh → Nhạc nền. File nhạc nằm ở `apps/client/public/audio/music/`; thiếu file nào thì im lặng, không lỗi.

Máy chủ làm việc của Claude không tải được file từ OpenGameArt, nên **bạn tải file về và thả vào thư mục trên** theo đúng tên ở bảng dưới. Không cần sửa code. Nếu muốn đổi bài cho map nào, sửa `public/audio/music/manifest.json` (mục `contexts`).

## A. Bộ CC0 (phát hành vào miền công cộng: dùng thương mại, không bắt buộc ghi công)

Đã kiểm trang tải của từng bài ngày 2026-10-29 (giấy phép ghi ngay trên trang).

| Dùng cho | Tên file đặt vào `public/audio/music/` | Bài, tác giả | Trang tải |
|---|---|---|---|
| Quảng Trường (`town`) | `town.mp3` (tải file `TownTheme.mp3`) | Town Theme RPG, cynicmusic, CC0 | https://opengameart.org/content/town-theme-rpg |
| Bìa Rừng (`forest`) | `forest.ogg` (trong zip `forest_whisper_theme.zip`, lấy bản OGG) | Forest Whisper Theme, CleytonKauffman, CC0 | https://opengameart.org/content/forest-whisper-theme |
| Rừng Sâu (`deep`) | `deep.ogg` (tải file `forest_2.ogg`) | Cathedral in the forest (ambient loop), congusbongus, CC0 | https://opengameart.org/content/cathedral-in-the-forest-ambient-loop |
| Trận đấu (`battle`) | `battle.mp3` (tải file `rbl.mp3`) | RPG Battle Loop, iamoneabe, CC0 | https://opengameart.org/content/rpg-battle-loop |
| Thắng trận (jingle `victory`) | `victory.wav` (tải file `Heavy_ConceptB.wav`) | Victory Fanfare Short, cynicmusic, CC0 | https://opengameart.org/content/victory-fanfare-short |
| Bài dự phòng cho Quảng Trường/Hoàng Môn | `palace.mp3` (tải `025_A_New_Town.mp3`) | A New Town (RPG Theme), cynicmusic, CC0 | https://opengameart.org/content/a-new-town-rpg-theme |

Chưa có bài CC0 phù hợp cho **Triệu Linh Điện** (cần không khí trang nghiêm, huyền ảo) và chưa chắc hợp cho **Hoàng Môn** (cung điện oai nghiêm): hai map này xin dùng bài MiniMax ở mục B. Trong lúc chưa có file, Triệu Linh Điện dùng bài của Hoàng Môn, rồi bài Quảng Trường; Hoàng Môn dùng bài Quảng Trường (chuỗi ưu tiên trong `manifest.json`).

Lưu ý khi dùng:
- Nghe thử trước khi đặt; các bài này khác nhịp và mức âm lượng. Nếu bài nào quá to/nhỏ, chỉnh số trong `manifest.json` → `gain` (0–1), không phải cắt lại file.
- Bài lặp tốt nhất là loại "loop" (Rừng Sâu, trận đấu). Nếu nghe thấy cú ngắt ở chỗ lặp, cắt đuôi/đầu bằng Audacity (xem mục C).
- Có thể dùng thay bài rừng ở trên bằng **Troubled Forest** (Eric Matyas, CC-BY 4.0, https://opengameart.org/content/troubled-forest-looping): bản này **bắt buộc ghi công** trong màn Giới thiệu/Credits: `"Troubled Forest" by Eric Matyas soundimage.org`. Không dùng nếu chưa có chỗ ghi công.
- Tránh bài CC-BY-SA (ví dụ "Level finish fanfares", jobromedia): điều khoản chia sẻ tương tự ràng buộc cả sản phẩm.

## B. Prompt cho MiniMax (gói Plus)

Mình chưa kiểm được chi tiết giao diện/giới hạn của gói Plus (độ dài tối đa, số lượt), nên các prompt dưới đây viết để dán thẳng vào ô mô tả phong cách; nếu giao diện đòi lời bài hát thì chọn chế độ không lời (instrumental) hoặc để trống. Chạy mỗi prompt 2–3 lần, chọn bản nghe tốt nhất. Mục tiêu 60–120 giây, nhạc cụ nhạc phổ thông (sáo, đàn hạc, dây, đàn phím), không giọng hát, không đoạn nói.

Khối chung (dán đầu mỗi prompt, tiếng Anh vì mô hình nghe tiếng Anh chuẩn hơn):

> Instrumental video game music for an HD-2D fantasy JRPG in the style of Octopath Traveler: warm orchestral-chiptune hybrid, expressive melody, no vocals, no spoken words, no sound effects, steady tempo, clean loop-friendly structure that ends on the same harmony it starts on.

1. **hall.mp3** (Triệu Linh Điện, trang nghiêm, huyền ảo)
> [Khối chung] Sacred summoning hall. Solemn and wondrous, slow 68 BPM. Harp arpeggios, soft choir pads, glockenspiel and celesta sparkles, warm low strings, a gentle rising motif that suggests a calling ritual. No drums. Minor-to-major lift in the second half.

2. **palace.mp3** (Hoàng Môn, cung điện)
> [Khối chung] Royal palace gate. Stately, noble and bright, 92 BPM. Soft brass motifs, string section, harpsichord, light marching snare, flutes answering the melody. Major key, confident but not aggressive.

3. **town.mp3** (Quảng Trường, nếu muốn cùng phong cách thay bài CC0)
> [Khối chung] Busy medieval market square at midday. Cheerful and lively, 112 BPM. Acoustic guitar, flute, accordion, hand drum, light pizzicato strings, bouncing bass. Major key, warm and welcoming.

4. **forest.mp3** (Bìa Rừng)
> [Khối chung] Calm sunlit forest edge for a beginner area. Peaceful and curious, 84 BPM. Soft flute, acoustic guitar plucks, light marimba, airy strings, gentle shaker. Major key, a little wonder, never tense.

5. **deep.mp3** (Rừng Sâu)
> [Khối chung] Deep mysterious forest. Dim and uneasy but beautiful, 72 BPM. Low sustained strings, muted harp, wooden flute with long breaths, soft pitched percussion like water drops, a distant cello line. Minor key, slowly shifting harmony.

6. **battle.mp3** (trận đấu)
> [Khối chung] Wild creature battle. Driving and exciting, 148 BPM. Fast strings ostinato, punchy brass hits, taiko-style drums, electric-guitar-free, heroic melody on top. Minor key with a heroic lift in the chorus. Loop-friendly.

7. **victory.ogg** (đoạn thắng, 4–8 giây)
> [Khối chung] A very short victory fanfare of 5 seconds: bright trumpet and strings play a rising phrase, a glittering harp glissando, ends on a clear resolved major chord with a short natural tail. No loop.

## C. Xử lý file nhạc (nếu cần)
- Cắt/loop: mở bằng Audacity, chọn đoạn, Effect → Crossfade Clips hoặc cắt đúng nhịp; xuất OGG Vorbis chất lượng 5–6 (≈160 kbps) hoặc MP3 192 kbps.
- Dung lượng: ưu tiên mỗi bài dưới 3 MB (tải một lần khi vào map, trình duyệt lưu đệm).
- Ghi lại nguồn và giấy phép của từng file vào `apps/client/public/audio/music/CREDITS.md` khi thêm (mẫu: tên bài, tác giả, giấy phép, link). File này không bắt buộc với CC0 nhưng nên có để sau này kiểm.
- Trình duyệt chặn tự phát nhạc đến khi người chơi chạm/nhấn lần đầu; nhạc bắt đầu ngay sau đó. Safari cần ít nhất một thao tác trên trang (đã xử lý).
