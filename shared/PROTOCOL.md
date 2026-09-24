# Phimond WebSocket Protocol (v0.1)

JSON, 1 message = 1 dòng. Field `type` luôn có. Server là authoritative — client chỉ gửi input, server mới thay đổi state.

## Client → Server

### HELLO
Gửi đầu tiên sau khi kết nối. Mở session cho player.
```json
{ "type": "HELLO", "name": "phileanh" }
```

### MOVE
Yêu cầu di chuyển 1 ô trong overworld (grid-based, 20×15).
```json
{ "type": "MOVE", "dir": "up" }
```
`dir` ∈ `"up" | "down" | "left" | "right"`.

### ACTION (Phase 2+ — placeholder)
```json
{ "type": "ACTION", "choice": "attack" }
{ "type": "ACTION", "choice": "skill", "skillId": "thunder_shock" }
{ "type": "ACTION", "choice": "item",   "itemId": "potion" }
{ "type": "ACTION", "choice": "flee" }
```

## Server → Client

### STATE
Broadcast khi có thay đổi vị trí player. MVP: chỉ render remote players (không cho mọi người điều khiển lẫn nhau).
```json
{
  "type": "STATE",
  "players": [
    { "name": "phileanh", "x": 5, "y": 7, "dir": "up" }
  ]
}
```

### ENCOUNTER (Phase 2+)
Trigger khi player bước vào tall grass zone và roll trúng encounter rate.

### BATTLE_START / BATTLE_TURN / BATTLE_END (Phase 2+)
Xem `IMPLEMENTATION_PLAN.md` mục 5.

### ERROR
```json
{ "type": "ERROR", "message": "Invalid direction" }
```

## Connection lifecycle
1. Client mở WebSocket
2. Server accept (không gửi gì — đợi client)
3. Client gửi `HELLO` đầu tiên
4. Server broadcast `STATE` mỗi khi player thay đổi vị trí
5. Đóng kết nối: server broadcast `STATE` không còn player đó

## Validation rules (server side)
- `HELLO.name`: 1–16 ký tự alphanumeric + underscore; nếu trùng tên thì reject (1 player per name MVP).
- `MOVE.dir`: phải ∈ 4 giá trị hợp lệ.
- Tất cả input khác ngoài HELLO trước HELLO → trả ERROR.
- Player position: clamp vào `[0, 20) × [0, 15)`.
