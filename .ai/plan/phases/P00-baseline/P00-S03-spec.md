# P00-S03 — Metrics, fault/load baseline và review phase

Scope: P00-R04/R06; implementation [T06–T07](P00-implementation-plan.md).

Player outcome: độ chậm được đo riêng giữa render, network và persistence; các sprint tối ưu sau có baseline thật để so sánh.

Acceptance: harness opt-in, ID/timeout/close/rejection tests; không pass khi thiếu active users hoặc stalled; báo số action/op và percentiles, không in secrets. Có baseline 1/10 account độc lập, reconnect nhóm nhỏ, client thật và report môi trường. CPU/full process RSS, network shaping, DB locks/slow queries và shared fan-out chưa đo phải ghi unmeasured.

Budget đề xuất từ master giữ nguyên: 50 CCU; RTT≤150ms/jitter≤30ms; server p95≤50ms/p99≤100ms; ack p95≤250ms/p99≤400ms; errors<0.1%; render 60Hz p95≤16.7ms/p99≤33.3ms. Config thử hiện tại local server + remote Aiven là baseline dev, không cấu hình release đã chốt. Không hạ gate nếu không đạt.

P00 không chứng nhận 50 CCU: shared-world chưa có. 2h soak, hot-map, 50 battles, stress75 và staging gần production thuộc P06/P09. Review phase phải ghi bottleneck, gameplay friction dưới tải và task tiếp theo; không suy từ bot pass thành no-lag.
