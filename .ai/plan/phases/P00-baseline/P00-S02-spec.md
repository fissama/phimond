# P00-S02 — Live combat presentation và recovery

Scope: P00-R02/R05/R06; implementation [T03–T05](P00-implementation-plan.md). Depends S01 restore point/reference. Không đổi battle math/capture odds/chi phí.

Player outcome: thấy feedback của đúng lượt, result cuối không mất trước khi trở lại world, reconnect không đánh lại effect.

Acceptance:
- Given auth/read/duplicate receipt, when state được trả, then events rỗng và không terminal replay.
- Given hai revision có event seq=1, then hiển thị cả hai batch đúng một lần.
- Given finishing action, then public terminal units còn để render dù authoritative battle=null; movement/contact/NPC/auto bị khóa đến hết feedback.
- Given disconnect/stale/malformed response, then state không rollback, pending đúng request và không retry mutation tự động.
- Given peaceful map wild_spawns=null, then world/contact không phát script error mỗi frame.

Contract additive: `data.presentation`, không private history/RNG/pet internals. Character save không migration. Giữ hướng/pivot và art nguồn. Kiểm thử Go WebSocket thật + Godot active scene + MySQL live/native; seeded fixtures phải ghi rõ không là progression tự nhiên.

Review gameplay: khả năng đọc lượt/target/result, thời gian chờ, input lock/recovery. Evidence ở verification và review phase; menu/balance redesign chuyển P02/P03.
